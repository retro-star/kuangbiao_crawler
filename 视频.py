#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :视频.py
# @Time      :2023/4/6 22:46
# @Author    :retro_star
import os

import requests
from threadpool import ThreadPool


class CrawlerOfVideo:
    def __init__(self, num, m3u8_url):
        self.m3u8_url = m3u8_url
        self.num = num
        self.m3u8_path = r'm3u8.txt'
        self.ts_dir = r'D:\python_work\crawler\file_ts'
        self.mp4_dir = r'D:\python_work\crawler\file_mp4'
        self.thread_pool = ThreadPool(10)
        self.ts_path_sorted = []

    def request(self, url):
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78"
        }
        try:
            resp = requests.get(url, headers=header)
            resp.close()
        except requests.exceptions.ConnectionError as e:
            resp = self.request(url)
        return resp

    def main(self):
        self.download_ts_to_file()

    def download_m3u8(self, content):
        with open(self.m3u8_path, 'w') as f:
            f.write(content)

    def download_ts_to_file(self):
        with open(self.m3u8_path, 'r') as f:
            for i in f.readlines():
                i = i.strip()
                if not i.startswith('#'):
                    ts_name = i.split('/')[-1].replace('.png', '.ts').strip()
                    url = self.m3u8_url.replace('index.m3u8', i.strip())
                    save_path = os.path.join(self.ts_dir, ts_name)
                    self.ts_path_sorted.append(save_path)
                    self.thread_pool.put(self.download_ts_task, url, save_path)
        self.thread_pool.run()
        self.thread_pool.join()
        self.combine_ts(self.num)

    def download_ts_task(self, url, save_path):
        resp = self.request(url)
        with open(save_path, 'wb') as f:
            f.write(resp.content)

    def combine_ts(self, num):
        num = str(int(num)).rjust(2, '0')
        file_name = f'嗜血狂袭第三季第{num}集.mp4'
        print(f'{file_name}合并开始')
        mp4_path = os.path.join(self.mp4_dir, file_name)
        with open(mp4_path, 'wb') as f:
            for ts_path in self.ts_path_sorted:
                with open(ts_path, 'rb') as f_ts:
                    f.write(f_ts.read())
        print(f'{file_name}合并完毕')
        self.clean_ts_file()

    def clean_ts_file(self):
        for ts_name in os.listdir(self.ts_dir):
            tem_path = os.path.join(self.ts_dir, ts_name)
            os.remove(tem_path)


if __name__ == '__main__':
    url_list = [
        'https://cdn.wls911.com:777/20220502/6STWGRo3/index.m3u8',
        'https://cdn.wls911.com:777/20220502/Qdc1SuO4/index.m3u8',
        'https://cdn.wls911.com:777/20220502/hpbNPhyN/index.m3u8',
        'https://cdn.wls911.com:777/20220502/K7Alc0r0/index.m3u8',
        'https://cdn.wls911.com:777/20220502/m6WuyRNi/index.m3u8',
        'https://cdn.wls911.com:777/20220502/EHQb0b3F/index.m3u8',
        'https://cdn.wls911.com:777/20220502/Xg2ke2bS/index.m3u8',
        'https://cdn.wls911.com:777/20220502/iROxzb0b/index.m3u8',
        'https://cdn.wls911.com:777/20220502/jnpGWJH3/index.m3u8',
        'https://cdn.wls911.com:777/20220502/2EklxKGw/index.m3u8',
    ]
    for index, url in enumerate(url_list):
        num = 1 + index
        instance = CrawlerOfVideo(num, url)
        instance.download_m3u8(instance.request(url).text)
        instance.main()
