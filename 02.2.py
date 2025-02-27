import sys
import os
import re
import mysql.connector
from mysql.connector import Error
from datetime import datetime


def check_and_add_columns(conn):
    """检查并添加必要的字段到数据库表中。

    参数:
        conn (mysql.connector.connection.MySQLConnection): 数据库连接对象。
    """
    cursor = conn.cursor()
    try:
        # 获取表结构
        cursor.execute("DESCRIBE movies")
        columns = [column[0] for column in cursor.fetchall()]

        # 需要添加的字段
        required_columns = {
            'length': 'INT',
            'director': 'VARCHAR(255)',
            'producer': 'VARCHAR(255)',
            'distributor': 'VARCHAR(255)',
            'categories': 'TEXT',
            'actors': 'TEXT',
            'update_time': 'DATETIME'
        }

        # 检查并添加缺失的字段
        for column, column_type in required_columns.items():
            if column not in columns:
                print(f"添加字段: {column}")
                cursor.execute(f"ALTER TABLE movies ADD COLUMN {column} {column_type}")
                conn.commit()
    except Error as e:
        print(f"添加字段失败: {e}")
    finally:
        cursor.close()


def find_items_in_files(directory, conn):
    """遍历指定目录下的所有文件，查找并处理相关内容。

    参数:
        directory (str): 要搜索的目录路径。
        conn (mysql.connector.connection.MySQLConnection): 数据库连接对象。
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            process_file(os.path.join(root, file), conn)


def process_file(file_path, conn):
    """处理单个文件的内容。

    参数:
        file_path (str): 文件的完整路径。
        conn (mysql.connector.connection.MySQLConnection): 数据库连接对象。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # 使用正则表达式匹配识别码
        code_match = re.search(r'<span class="header">識別碼:</span> <span style="color:#CC0000;">(.*?)</span>',
                               content)
        if code_match:
            code = code_match.group(1)
            print(f"找到识别码: {code}")

            # 使用正则表达式匹配长度信息
            length_match = re.search(r'<span class="header">長度:</span> (\d+)分鐘', content)
            if length_match:
                length = int(length_match.group(1))
                print(f"找到长度信息: {length} 分钟")
            else:
                length = None
                print("未找到长度信息。")

            # 使用正则表达式匹配导演信息
            director_match = re.search(r'<span class="header">導演:</span> <a href=".*?">(.*?)</a>', content)
            if director_match:
                director = director_match.group(1)
                print(f"找到导演信息: {director}")
            else:
                director = None
                print("未找到导演信息。")

            # 使用正则表达式匹配制作商信息
            producer_match = re.search(r'<span class="header">製作商:</span> <a href=".*?">(.*?)</a>', content)
            if producer_match:
                producer = producer_match.group(1)
                print(f"找到制作商信息: {producer}")
            else:
                producer = None
                print("未找到制作商信息。")

            # 使用正则表达式匹配发行商信息
            distributor_match = re.search(r'<span class="header">發行商:</span> <a href=".*?">(.*?)</a>', content)
            if distributor_match:
                distributor = distributor_match.group(1)
                print(f"找到发行商信息: {distributor}")
            else:
                distributor = None
                print("未找到发行商信息。")

            # 使用正则表达式匹配类别信息
            category_matches = re.findall(
                r'<span class="genre"><label><input type="checkbox" name="gr_sel" value=".*?"><a href=".*?">(.*?)</a></label></span>',
                content)
            if category_matches:
                categories = ', '.join(category_matches)
                print(f"找到类别信息: {categories}")
            else:
                categories = None
                print("未找到类别信息。")

            # 使用正则表达式匹配演员信息
            actor_matches = re.findall(r'<div class="star-name"><a href=".*?" title=".*?">(.*?)</a></div>', content)
            if actor_matches:
                actors = ', '.join(actor_matches)
                print(f"找到演员信息: {actors}")
            else:
                actors = None
                print("未找到演员信息。")

            # 更新数据库中的信息
            update_movie_info(code, length, director, producer, distributor, categories, actors, conn)


def update_movie_info(code, length, director, producer, distributor, categories, actors, conn):
    """根据识别码更新电影的信息。

    参数:
        code (str): 识别码。
        length (int): 长度（分钟）。
        director (str): 导演。
        producer (str): 制作商。
        distributor (str): 发行商。
        categories (str): 类别。
        actors (str): 演员。
        conn (mysql.connector.connection.MySQLConnection): 数据库连接对象。
    """
    cursor = conn.cursor()
    try:
        sql = "UPDATE movies SET length = %s, director = %s, producer = %s, distributor = %s, categories = %s, actors = %s, update_time = %s WHERE code = %s"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(sql, (length, director, producer, distributor, categories, actors, current_time, code))
        conn.commit()
        print(f"识别码为 {code} 的电影信息更新成功。")
    except Error as e:
        print(f"更新失败: {e}")
    finally:
        cursor.close()


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--dir':
        print("用法: python script.py --dir <目录路径>")
        exit(1)

    directory = sys.argv[2]
    if not os.path.isdir(directory):
        print(f"{directory} 不是一个有效的目录。")
        exit(1)

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # 你的数据库用户名
            password='root123',  # 你的数据库密码
            database='movie_db'  # 你的数据库名
        )
        print("数据库连接成功！")

        # 检查并添加必要的字段
        check_and_add_columns(conn)

        # 在这里调用文件处理函数，并传递数据库连接对象
        find_items_in_files(directory, conn)

    except Error as err:
        print(f"数据库连接失败: {err}")
        exit(1)  # 如果连接失败，退出程序
    finally:
        if conn.is_connected():
            conn.close()
            print("数据库连接已关闭。")
