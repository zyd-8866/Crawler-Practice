import os
import sys
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime

# 尝试连接到 MySQL 数据库
try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # 你的数据库用户名
        password='root123',  # 你的数据库密码
        database='movie_db'  # 你的数据库名
    )
    print("数据库连接成功！")
except mysql.connector.Error as err:
    print(f"数据库连接失败: {err}")
    exit(1)  # 如果连接失败，退出程序

# 创建游标对象
c = conn.cursor()

# 检查 movies 表是否存在
c.execute("""
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 'movie_db'
      AND TABLE_NAME = 'movies'
""")
if c.fetchone()[0] == 0:
    # 创建 movies 表
    c.execute("""
        CREATE TABLE movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(255) NOT NULL UNIQUE,
            name VARCHAR(255),
            release_date DATE,
            has_hd VARCHAR(255),
            has_subtitle VARCHAR(255),
            cover_image VARCHAR(255),
            update_time TIMESTAMP
        )
    """)
    conn.commit()
    print("movies 表已创建。")

# 检查 update_time 列是否存在
c.execute("""
    SELECT COUNT(*)
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'movie_db'
      AND TABLE_NAME = 'movies'
      AND COLUMN_NAME = 'update_time'
""")
if c.fetchone()[0] == 0:
    # 添加 update_time 列
    c.execute("""
        ALTER TABLE movies
        ADD COLUMN update_time TIMESTAMP
    """)
    conn.commit()
    print("update_time 列已添加。")


def parse_item(item):
    # 提取封面图片
    img_tag = item.find('img')
    cover_image = img_tag['src'] if img_tag else ''

    # 提取名称
    title_tag = item.find('span')
    name = title_tag.text.strip().split('\n')[0] if title_tag else None

    # 提取番号
    code = title_tag.find('date').text.strip() if title_tag and title_tag.find('date') else None

    # 提取发售日期
    release_date = title_tag.find_all('date')[-1].text.strip() if title_tag and len(
        title_tag.find_all('date')) > 1 else None
    # 处理无效日期
    if release_date == '0000-00-00':
        release_date = None

    # 检查是否存在高清磁力链接
    hd_button = item.find('button', class_='btn btn-xs btn-primary')
    has_hd = "存在" if hd_button else "不存在"

    # 检查是否存在中文磁力链接
    subtitle_button = item.find('button', class_='btn btn-xs btn-warning')
    has_subtitle = "存在" if subtitle_button else "不存在"

    return {
        'code': code,
        'name': name,
        'release_date': release_date,
        'has_hd': has_hd,
        'has_subtitle': has_subtitle,
        'cover_image': cover_image
    }


def find_div_content(directory, tag_id):
    file_count = 0
    total_item_count = 0
    total_insert_count = 0
    total_update_count = 0

    # 遍历目录下的所有文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # 确保只处理文本文件
        if os.path.isfile(file_path) and file_path.endswith('.txt'):
            file_count += 1
            print(f"正在处理文件: {filename}")

            with open(file_path, 'r', encoding='utf-8') as file:
                # 读取文件内容
                content = file.read()

                # 使用BeautifulSoup解析HTML内容
                soup = BeautifulSoup(content, 'html.parser')

                # 查找指定的标签内容
                div = soup.find('div', id=tag_id)

                if div:
                    # 解析每个item
                    items = div.find_all('div', class_='item')
                    file_item_count = 0
                    file_insert_count = 0
                    file_update_count = 0

                    for i, item in enumerate(items, start=1):
                        movie_data = parse_item(item)
                        file_item_count += 1
                        total_item_count += 1

                        # 更新时间
                        update_time = datetime.now()

                        # 检查记录是否已经存在
                        c.execute("""
                            SELECT COUNT(*)
                            FROM movies
                            WHERE code = %s
                        """, (movie_data['code'],))
                        record_exists = c.fetchone()[0] > 0

                        if record_exists:
                            # 更新记录
                            c.execute("""
                                UPDATE movies
                                SET name = %s,
                                    release_date = %s,
                                    has_hd = %s,
                                    has_subtitle = %s,
                                    cover_image = %s,
                                    update_time = %s
                                WHERE code = %s
                            """, (movie_data['name'], movie_data['release_date'], movie_data['has_hd'],
                                  movie_data['has_subtitle'], movie_data['cover_image'], update_time,
                                  movie_data['code']))
                            file_update_count += 1
                            total_update_count += 1
                            print(f"第 {i} 条记录更新成功，番号是: {movie_data['code']}")
                        else:
                            # 插入新记录
                            c.execute("""
                                INSERT INTO movies (code, name, release_date, has_hd, has_subtitle, cover_image, update_time)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """, (
                            movie_data['code'], movie_data['name'], movie_data['release_date'], movie_data['has_hd'],
                            movie_data['has_subtitle'], movie_data['cover_image'], update_time))
                            file_insert_count += 1
                            total_insert_count += 1
                            print(f"第 {i} 条记录插入成功，番号是: {movie_data['code']}")

                    print(
                        f"文件 {filename} 中找到 {file_item_count} 条有效数据，{file_insert_count} 条记录插入成功，{file_update_count} 条记录更新成功。")
                else:
                    print(f"文件 {filename} 中未找到 {tag_id} 标签的内容。")

    # 提交事务
    conn.commit()
    # 关闭数据库连接
    conn.close()

    print(
        f"成功读取 {file_count} 个文件，找到 {total_item_count} 个标记，{total_insert_count} 条记录插入成功，{total_update_count} 条记录更新成功。")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--dir':
        print("用法: python script.py --dir <目录路径>")
        exit(1)

    directory = sys.argv[2]
    if not os.path.isdir(directory):
        print(f"{directory} 不是一个有效的目录。")
        exit(1)

    find_div_content(directory, 'waterfall')
