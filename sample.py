from selenium import webdriver
import time
import os.path
import requests
import hashlib
import random
import json
#from SaYi.src.plugins.dataset_controller import DataSetControl

url = "https://algcontest.rainng.com/"
job_path = "C:\\Users\\DZYCD\\PycharmProjects\\SaYibot\\SaYi\\src\\plugins\\time_freezer\\job_list.json"
#dataset = DataSetControl(job_path)


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
    pass


def get_contest_list(check_oj=None):
    if check_oj is None:
        check_oj = ["LuoGu", "NowCoder", "CodeForces", "LeetCode", "JiSuanKe"]
    contest = get_dic()
    contest_list = []
    for i in contest:
        print(i)
        if i["oj"] in check_oj:
            info = [i["oj"], i["name"], i["startTime"], i["endTime"], i["status"], i["oiContest"], i["link"]]
            contest_list.append(info)
            add_into_job(info)
    return contest_list


get_contest_list()
