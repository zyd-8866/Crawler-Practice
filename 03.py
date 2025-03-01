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

def log_failed_video(video_id):
    try:
        # 将失败的视频番号写入文件
        with open("download_video_err.txt", "a", encoding="utf-8") as error_file:
            error_file.write(f"{video_id}\n")
        print(f"错误的番号已写入到 download_video_err.txt: {video_id}")
    except Exception as e:
        print(f"记录失败的视频番号时发生错误: {e}")

def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5,proxies=proxies,headers=headers)  # 发送 HEAD 请求
        print(f"请求 URL: {url}")  # 打印请求的 URL，便于调试
        if response.status_code == 200:
            print(f"[✔] 网址有效: {url}")
            return url  # 返回有效链接
        elif response.status_code == 403:
            print(f"[⚠️] 网址被禁止访问 (状态码 403): {url}，重新尝试一次")
            return check_url(url)  # 重新尝试
        else:
            #print(f"[✘] 网址无效 (状态码 {response.status_code}): {url}")

            return None  # 如果是其他状态码（如 404），认为链接无效
    except requests.RequestException as e:
        print(f"[✘] 请求错误: {e} - {url}")
        return None

def rule_2(code):
    match = re.match(r'([A-Za-z]+)-(\d+)', code)
    if match:  # 确保匹配成功
        prefix = match.group(1).lower()  # 取出前缀并转换为小写
        num = match.group(2)  # 取出 ID
        moren = 'https://cc3001.dmm.co.jp/litevideo/freepv/'
        print('前缀是：', prefix)
        print('ID是：', num)
        first_1 = prefix[0]
        print('前缀第一个字母：', first_1)
        first_2 = prefix[:2]
        print('前缀前二个字母：', first_2)
        first_3 = prefix[:3]
        print('前缀前三个字母：', first_3)
        shuzi_5 = num.zfill(5)
        print('数字补到5位：', shuzi_5)
        houzui1='mhb'
        houzui2='_mhb_w'
        houzui3='dmb'
        houzui4='_dmb_w'

        rule_1_url = f"{moren}{first_1}/{first_3}/{prefix}{shuzi_5}/{prefix}{shuzi_5}{houzui1}.mp4"
        rule_2_url = f"{moren}{first_1}/{first_3}/{prefix}{shuzi_5}/{prefix}{shuzi_5}{houzui2}.mp4"
        rule_3_url = f"{moren}{first_1}/{first_3}/{prefix}{shuzi_5}/{prefix}{shuzi_5}{houzui3}.mp4"
        rule_4_url = f"{moren}{first_1}/{first_3}/{prefix}{shuzi_5}/{prefix}{shuzi_5}{houzui4}.mp4"
        rule_5_url = f"{moren}{first_1}/{first_3}/{prefix}{num}/{prefix}{num}{houzui1}.mp4"
        rule_6_url = f"{moren}{first_1}/{first_3}/{prefix}{num}/{prefix}{num}{houzui2}.mp4"
        rule_7_url = f"{moren}{first_1}/{first_3}/{prefix}{num}/{prefix}{num}{houzui3}.mp4"
        rule_8_url = f"{moren}{first_1}/{first_3}/{prefix}{num}/{prefix}{num}{houzui4}.mp4"
        rule_9_url = f"{moren}h/h_2/h_237{prefix}{num}/h_237{prefix}{num}{houzui1}.mp4"
        rule_10_url = f"{moren}h/h_2/h_237{prefix}{num}/h_237{prefix}{num}{houzui2}.mp4"
        rule_11_url = f"{moren}h/h_2/h_237{prefix}{num}/h_237{prefix}{num}{houzui3}.mp4"
        rule_12_url = f"{moren}h/h_2/h_237{prefix}{num}/h_237{prefix}{num}{houzui4}.mp4"
        rule_13_url = f"{moren}1/1{first_2}/1{prefix}{num}/1{prefix}{num}{houzui1}.mp4"
        rule_14_url = f"{moren}1/1{first_2}/1{prefix}{num}/1{prefix}{num}{houzui2}.mp4"
        rule_15_url = f"{moren}1/1{first_2}/1{prefix}{num}/1{prefix}{num}{houzui3}.mp4"
        rule_16_url = f"{moren}1/1{first_2}/1{prefix}{num}/1{prefix}{num}{houzui4}.mp4"
        rule_17_url = f"{moren}h/h_1/h_1345{prefix}{shuzi_5}/h_1345{prefix}{shuzi_5}{houzui1}.mp4"
        rule_18_url = f"{moren}h/h_1/h_1345{prefix}{shuzi_5}/h_1345{prefix}{shuzi_5}{houzui2}.mp4"
        rule_19_url = f"{moren}h/h_1/h_1345{prefix}{shuzi_5}/h_1345{prefix}{shuzi_5}{houzui3}.mp4"
        rule_20_url = f"{moren}h/h_1/h_1345{prefix}{shuzi_5}/h_1345{prefix}{shuzi_5}{houzui4}.mp4"
        rule_21_url = f"{moren}1/13{first_1}/13{prefix}{num}/13{prefix}{num}{houzui1}.mp4"
        rule_22_url = f"{moren}1/13{first_1}/13{prefix}{num}/13{prefix}{num}{houzui2}.mp4"
        rule_23_url = f"{moren}1/13{first_1}/13{prefix}{num}/13{prefix}{num}{houzui3}.mp4"
        rule_24_url = f"{moren}1/13{first_1}/13{prefix}{num}/13{prefix}{num}{houzui4}.mp4"
        rule_25_url = f"{moren}1/118/118{prefix}{num}/118{prefix}{num}{houzui1}.mp4"
        rule_26_url = f"{moren}1/118/118{prefix}{num}/118{prefix}{num}{houzui2}.mp4"
        rule_27_url = f"{moren}1/118/118{prefix}{num}/118{prefix}{num}{houzui3}.mp4"
        rule_28_url = f"{moren}1/118/118{prefix}{num}/118{prefix}{num}{houzui4}.mp4"
        rule_29_url = f"{moren}4/49e/49{prefix}{num}/49{prefix}{num}{houzui1}.mp4"
        rule_30_url = f"{moren}4/49e/49{prefix}{num}/49{prefix}{num}{houzui2}.mp4"
        rule_31_url = f"{moren}4/49e/49{prefix}{num}/49{prefix}{num}{houzui3}.mp4"
        rule_32_url = f"{moren}4/49e/49{prefix}{num}/49{prefix}{num}{houzui4}.mp4"
        rule_33_url = f"{moren}1/1{first_2}/1{prefix}{shuzi_5}/1{prefix}{shuzi_5}{houzui1}.mp4"
        rule_34_url = f"{moren}1/1{first_2}/1{prefix}{shuzi_5}/1{prefix}{shuzi_5}{houzui2}.mp4"
        rule_35_url = f"{moren}1/1{first_2}/1{prefix}{shuzi_5}/1{prefix}{shuzi_5}{houzui3}.mp4"
        rule_36_url = f"{moren}1/1{first_2}/1{prefix}{shuzi_5}/1{prefix}{shuzi_5}{houzui4}.mp4"
        rule_37_url = f"{moren}8/84{first_1}/84{prefix}{num}/84{prefix}{num}{houzui1}.mp4"
        rule_38_url = f"{moren}8/84{first_1}/84{prefix}{num}/84{prefix}{num}{houzui2}.mp4"
        rule_39_url = f"{moren}8/84{first_1}/84{prefix}{num}/84{prefix}{num}{houzui3}.mp4"
        rule_40_url = f"{moren}8/84{first_1}/84{prefix}{num}/84{prefix}{num}{houzui4}.mp4"
        rule_41_url = f"{moren}h/h_1/h_139{prefix}{num}/h_139{prefix}{num}{houzui1}.mp4"
        rule_42_url = f"{moren}h/h_1/h_139{prefix}{num}/h_139{prefix}{num}{houzui2}.mp4"
        rule_43_url = f"{moren}h/h_1/h_139{prefix}{num}/h_139{prefix}{num}{houzui3}.mp4"
        rule_44_url = f"{moren}h/h_1/h_139{prefix}{num}/h_139{prefix}{num}{houzui4}.mp4"
        #print('规则1：',rule_1_url)
        valid_url = check_url(rule_1_url)
        if valid_url:
            return valid_url
        #print('规则2：', rule_2_url)
        valid_url = check_url(rule_2_url)
        if valid_url:
            return valid_url
        #print('规则3：', rule_3_url)
        valid_url = check_url(rule_3_url)
        if valid_url:
            return valid_url
        #print('规则4：', rule_4_url)
        valid_url = check_url(rule_4_url)
        if valid_url:
            return valid_url
        #print('规则5：', rule_5_url)
        valid_url = check_url(rule_5_url)
        if valid_url:
            return valid_url
        #print('规则6：', rule_6_url)
        valid_url = check_url(rule_6_url)
        if valid_url:
            return valid_url
        #print('规则7：', rule_7_url)
        valid_url = check_url(rule_7_url)
        if valid_url:
            return valid_url
        #print('规则8：', rule_8_url)
        valid_url = check_url(rule_8_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_9_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_10_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_11_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_12_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_13_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_14_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_15_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_16_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_17_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_18_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_19_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_20_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_21_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_22_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_23_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_24_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_25_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_26_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_27_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_28_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_29_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_30_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_31_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_32_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_33_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_34_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_35_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_36_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_37_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_38_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_39_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_40_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_41_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_42_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_43_url)
        if valid_url:
            return valid_url
        valid_url = check_url(rule_44_url)
        if valid_url:
            return valid_url
        print('未匹配到规则,写入错误文件夹')
        log_failed_video(code)
    else:
        print("Invalid code format")

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
                            urlyes=rule_2(line.strip())
                            if urlyes:
                                print('成功获取到正确URL：',urlyes,'    --调用下载')
                                type_nama= line.strip()+".mp4"
                                download_video(urlyes, type_nama, line.strip())
                            else:
                                print("未能获取有效 URL，跳过下载步骤")
                    print(f"错误：文件 '{arg}' 未找到。")
                except Exception as e:
                    print(f"处理文件 '{arg}' 时发生错误: {e}")
            else:
                # 如果不是文件，则直接输出参数
                print("当前番号是:",arg)
                urlyes = rule_2(arg)
                if urlyes:
                    #print(urlyes)
                    print('成功获取到正确URL：',urlyes,'    --调用下载')
                    type_nama = arg+".mp4"
                    download_video(urlyes, type_nama, arg)
                else:
                    print("未能获取有效 URL，跳过下载步骤")
    else:
        print("请提供至少一个参数。")

if __name__ == "__main__":
    main()
