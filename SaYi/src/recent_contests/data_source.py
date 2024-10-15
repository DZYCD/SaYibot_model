#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# Copyright (C) 2024 - 2024 heihieyouheihei, Inc. All Rights Reserved
#
# @Time    : 2024/10/15 下午10:28
# @Author  : 单子叶蚕豆_DzyCd
# @File    : test.py
# @IDE     : PyCharm
from selenium import webdriver
import time
import os.path
import requests
import hashlib
import random
import json
from ..dataset_controller import DataSetControl

url = "https://algcontest.rainng.com/"
job_path = "C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\plugins\\time_freezer\\job_list.json"
dataset = DataSetControl(job_path)


def get_dic():
    dic = requests.get(url)
    # print(web)
    return json.loads(dic.text)


def to_date(seconds):
    timeArray = time.localtime(seconds)  # 秒数
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def to_minutes(seconds):
    return str(seconds//60)


def add_into_job(info):
    job_info = [info[2], info[0]+"_contest_annotation", info[1], info[6]]
    dataset_list = dataset.get_value("result", "job_list")
    flag = 1
    for p in dataset_list:
        try:
            if p[3] == job_info[3]:
                p[2] = job_info[2]
                p[1] = job_info[1]
                p[0] = job_info[0]
                flag = 0
        except:
            pass
    if flag:
        dataset_list.append(job_info)
    dataset_list.sort(key=lambda x: x[0], reverse=False)
    dataset.update_value("result", "job_list", dataset_list)
    dataset.update_value("result", "job_count", len(dataset_list))


trans = {
    "Register": "正在报名",
    "Public": "公开展示",
    "Running": "正在进行"
}


def get_contest_list(check_oj=None):
    if check_oj is None:
        check_oj = ["LuoGu", "NowCoder", "CodeForces", "LeetCode", "JiSuanKe"]
    contest = get_dic()
    contest_list = []
    for i in contest:
        if i["oj"] in check_oj:
            info = [i["oj"], i["name"], i["startTimeStamp"], i["endTimeStamp"], trans[i["status"]], i["oiContest"], i["link"]]
            contest_list.append(info)
            if i["status"] == "Running":
                continue
            add_into_job(info)
    return contest_list
