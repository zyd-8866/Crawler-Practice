import sys
import re
import os
import requests
from tensorflow.python.data.experimental.ops.testing import sleep
from tqdm import tqdm
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# 代理设置
proxies = {
    'http': 'socks5://127.0.0.1:10808',
    'https': 'socks5://127.0.0.1:10808'
}

# 设置请求头
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

def rule_1(code):
    # 提取前缀和数字部分
    match = re.match(r'([A-Za-z]+)-(\d+)', code)
    if match:
        prefix = match.group(1).lower()  # 提取前缀并转小写
        num = match.group(2)  # 提取数字，不做补齐处理

        # 特殊处理：如果是前缀为 SW，则构建链接时加上 '1' 作为前缀，不补齐数字
        if prefix == "sw":
            return f"https://cc3001.dmm.co.jp/litevideo/freepv/1/1{prefix}/1{prefix}{num}/1{prefix}{num}_dmb_w.mp4"

        # 对于其他前缀，按照常规方式补齐数字至5位
        num = num.zfill(5)  # 补齐数字部分至 5 位
        prefix_dir = prefix[:1] + "/" + prefix[:3]  # 比如 "d/das"

        # 根据规则生成链接
        return f"https://cc3001.dmm.co.jp/litevideo/freepv/{prefix_dir}/{prefix}{num}/{prefix}{num}mhb.mp4"
    else:
        return "Invalid code format"


def download_video(url, dest_path,name_fanhao):
    try:
        # 获取文件名
        filename = os.path.basename(dest_path)
        download_dir = os.path.join(os.getcwd(), 'download_video')
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # 构造下载路径
        dest_path = os.path.join(download_dir, name_fanhao+".mp4")
        # 发起请求，获取文件内容
        with requests.get(url, stream=True, proxies=proxies, headers=headers) as r:
            r.raise_for_status()  # 检查请求是否成功（如果失败，会抛出HTTPError）

            # 获取文件总大小
            total_size = int(r.headers.get('content-length', 0))

            # 设置进度条
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as bar:
                with open(dest_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):  # 每次写入8KB数据
                        f.write(chunk)
                        bar.update(len(chunk))  # 更新进度条

        print(f"下载完成：{dest_path}")
        print('更新数据库')
        update_data_in_db(name_fanhao,url)
        print('等待1s防止网络错误')
        sleep(1)

        return True
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 错误：{e}")
        log_failed_video(name_fanhao)
        return False
    except requests.exceptions.RequestException as e:
        print(f"请求错误：{e}")
        log_failed_video(name_fanhao)
        return False
    except Exception as e:
        print(f"下载发生未知错误：{e}")
        log_failed_video(name_fanhao)
        return False

def log_failed_video(video_id):
    try:
        # 将失败的视频番号写入文件
        with open("download_video_err.txt", "a", encoding="utf-8") as error_file:
            error_file.write(f"{video_id}\n")
        print(f"错误的番号已写入到 download_video_err.txt: {video_id}")
    except Exception as e:
        print(f"记录失败的视频番号时发生错误: {e}")


def update_data_in_db(name_fanhao, url):
    try:
        # 连接数据库
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # 数据库用户名
            password='root123',  # 数据库密码
            database='movie_db'  # 数据库名称
        )

        if conn.is_connected():
            print("数据库连接成功！")

            # 创建游标对象
            cursor = conn.cursor()

            # 获取当前时间
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # SQL 更新语句
            update_query = """
                UPDATE movies
                SET video_preview_download = %s, update_time = %s
                WHERE code = %s
            """

            # 执行更新操作
            cursor.execute(update_query, (url, current_time, name_fanhao))

            # 提交更改
            conn.commit()

            print(f"更新成功: 番号 {name_fanhao} 的预览视频链接已更新。")

            # 关闭游标
            cursor.close()

    except Error as err:
        print(f"数据库操作失败: {err}")

    finally:
        # 确保连接被关闭
        if conn.is_connected():
            conn.close()
            print("数据库连接已关闭。")


def main():
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            # 判断参数是否为文件
            if arg.endswith('.txt'):
                try:
                    # 尝试以只读模式打开文件
                    with open(arg, 'r', encoding='utf-8') as file:
                        # 逐行读取并打印文件内容
                        for line in file:
                            print("当前番号是:",line.strip())
                            download_video_url= rule_1(line.strip())
                            print("规则1输出的链接是:", download_video_url)
                            type_nama= line.strip()+".mp4"
                            print("调用下载：")
                            download_video(download_video_url,type_nama,line.strip())
                    print(f"错误：文件 '{arg}' 未找到。")
                except Exception as e:
                    print(f"处理文件 '{arg}' 时发生错误: {e}")
            else:
                # 如果不是文件，则直接输出参数
                print("当前番号是:",arg)
                download_video_url = rule_1(arg)
                print("规则1输出的链接是:", download_video_url)
                type_nama = arg+".mp4"
                print("调用下载：")
                download_video(download_video_url, type_nama,arg)

    else:
        print("请提供至少一个参数。")




if __name__ == "__main__":
    main()
