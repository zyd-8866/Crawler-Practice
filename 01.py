import os
import sys
import time
import requests

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


def sanitize_filename(url):
    # 去掉协议头和www，替换特殊字符，并加上.txt扩展名
    filename = url.replace('https://', '').replace('http://', '').replace('www.', '').replace('/', '-')
    return f"{filename}.txt"


def save_response_to_file(response, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)
    print(f"写入成功，文件路径是 {filename}")


def request_url(url):
    try:
        response = requests.get(url, proxies=proxies, headers=headers)
        response.raise_for_status()
        return response, None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def main():
    if len(sys.argv) < 3 or sys.argv[1] != '-u':
        print("用法:")
        print("  python xxx.py -u <URL>")
        print("  python xxx.py -u <URL> -start <开始编号> -stop <结束编号>")
        print("  python xxx.py -u <URL> --file <错误文件>")
        exit(1)

    url = sys.argv[2]
    start = None
    stop = None
    error_file = 'err.txt'

    if '-start' in sys.argv and '-stop' in sys.argv:
        start_index = sys.argv.index('-start')
        stop_index = sys.argv.index('-stop')
        start = int(sys.argv[start_index + 1])
        stop = int(sys.argv[stop_index + 1]) + 1  # 包含stop
    elif '--file' in sys.argv:
        file_index = sys.argv.index('--file')
        error_file = sys.argv[file_index + 1]

    if start is not None and stop is not None:
        for i in range(start, stop):
            current_url = f"{url}{i}"
            print(f"正在请求 URL: {current_url}")
            response, error = request_url(current_url)
            if response:
                print(f"请求成功: {current_url}")
                filename = sanitize_filename(current_url)
                print(f"正在写入文件: {filename}")
                save_response_to_file(response, filename)
            else:
                with open(error_file, 'a', encoding='utf-8') as err_file:
                    err_file.write(f"{i}\n")
                print(f"请求错误: {current_url}，原因: {error}")
            time.sleep(1)
    elif '--file' in sys.argv:
        if not os.path.exists(error_file):
            print(f"错误文件 {error_file} 不存在。")
            exit(1)

        with open(error_file, 'r', encoding='utf-8') as err_file:
            lines = err_file.readlines()

        new_error_file = 'err2.txt'
        for line in lines:
            i = line.strip()
            current_url = f"{url}{i}"
            print(f"正在请求 URL: {current_url}")
            response, error = request_url(current_url)
            if response:
                print(f"请求成功: {current_url}")
                filename = sanitize_filename(current_url)
                print(f"正在写入文件: {filename}")
                save_response_to_file(response, filename)
            else:
                with open(new_error_file, 'a', encoding='utf-8') as new_err_file:
                    new_err_file.write(f"{i}\n")
                print(f"请求错误: {current_url}，原因: {error}")
            time.sleep(1)
    else:
        print(f"正在请求 URL: {url}")
        response, error = request_url(url)
        if response:
            print(f"请求成功: {url}")
            filename = sanitize_filename(url)
            print(f"正在写入文件: {filename}")
            save_response_to_file(response, filename)
        else:
            print(f"请求错误: {url}，原因: {error}")


if __name__ == "__main__":
    main()
