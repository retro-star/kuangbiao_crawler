#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :狂飙.py
# @Time      :2023/2/11 22:18
# @Author    :retro_star
import os
import re

import requests
from concurrent.futures import ThreadPoolExecutor, wait
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def get(url):
    header = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78"
    }
    resp = requests.get(url, headers=header)
    return resp


def get_iframe(episode_url, episode_num):
    web = Chrome()
    web.get(episode_url)
    test = web.find_element(by=By.XPATH, value='//*[@id="playleft"]/iframe')
    m3u8_url = test.get_attribute("src")
    true_m3u8_url_re = re.compile(r"url=(?P<true_m3u8_url_group>.*)")
    true_m3u8_url = true_m3u8_url_re.search(m3u8_url).group("true_m3u8_url_group")
    print(f"开始下载第{episode_num}集m3u8文件")
    print(true_m3u8_url)
    get_ts_video(true_m3u8_url, episode_num)


def get_episodes(website_url):
    print("开始下载集数信息")
    resp = get(website_url)
    list_episodes_re = re.compile(r'href="(/play.*?)">第(\d+)集')
    list_episodes = list_episodes_re.findall(resp.text)[40:]
    s = 'http://ajuvip.com'
    for i in list_episodes:
        i_url = i[0]
        i_num = i[1]
        temp_episode = s + i_url
        print(f"开始获取第{i_num}集的iframe")
        get_iframe(temp_episode, i_num)


def get_ts_video(m3u8_url, episode_num):
    resp = get(m3u8_url)
    with open("m3u8.txt", "w", encoding="utf-8") as f:
        f.write(resp.text)
    resp.close()
    pool = ThreadPoolExecutor(40)
    task_list = []
    with open("m3u8.txt", "r", encoding='utf-8') as f:
        for i in f.readlines():
            if "#" not in i:
                ts_url = m3u8_url.replace("index.m3u8", i.strip())
                task_list.append(pool.submit(download_ts, ts_url, i))
        wait(task_list)
    pool.shutdown()
    merge_ts("m3u8.txt", episode_num)


def download_ts(ts_url, i):
    print(f"开始下载ts文件{i}", end="")
    resp_ts = get(ts_url)
    file_name = os.path.join("file_ts", i.strip())
    with open(file_name, "wb") as ts:
        ts.write(resp_ts.content)
    resp_ts.close()


def merge_ts(m3u8_file, num):
    print("开始合并视频文件")
    with open(m3u8_file, "r") as f:
        for i in f.readlines():
            if not i.startswith("#"):
                list = os.path.join(r"D:\python_work\crawler\file_ts", i.strip())
                with open(rf"file_mp4\狂飙第{num}集.mp4", 'ab') as out_file:
                    with open(list, 'rb') as need_file:
                        out_file.write(need_file.read())
                os.remove(list)


if __name__ == '__main__':
    url = "http://ajuvip.com/play/76129-2-1.html"
    get_episodes(url)
