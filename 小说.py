#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :小说.py
# @Time      :2023/10/24 22:47
# @Author    :retro_star
import time

import requests
import re
from threadpool import ThreadPool


class CrawlerOfText:
    def __init__(self):
        self.thread_pool = ThreadPool(6)
        self.main()

    @staticmethod
    def request(url):
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78"
        }
        resp = requests.get(url, headers=header)
        return resp

    @staticmethod
    def save(title, content):
        with open('舔狗反派只想苟女主不按套路走.txt', 'a', encoding='utf-8') as f:
            f.write(title)
            f.write('\n')
            for i in content:
                f.write(i)
                f.write('\n')

    def main(self):
        url = 'https://iyueba.net'
        temp_url = '/book_17202477/zj_168272973'
        while True:
            resp = self.request(url + temp_url)
            html = resp.text
            title_compile = re.compile('<h1 class="bookname">(.*?)</h1>')
            title = title_compile.search(html).group(1)
            content_compile = re.compile('<p>(.*?)</p>')
            content = content_compile.findall(html)
            self.save(title, content[1:])
            print(title)
            next_page_compile = re.compile('<a rel="(prev|next)" href="(.*?)">下一(页|章)</a>')
            try:
                temp_url = next_page_compile.search(html).group(2)
            except Exception as e:
                print(html)
                raise e
            time.sleep(0.1)


if __name__ == '__main__':
    CrawlerOfText()
