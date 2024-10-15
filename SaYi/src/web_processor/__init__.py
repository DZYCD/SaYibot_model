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
from selenium.webdriver.chrome.service import Service


def webshot(name, saveImgName):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    service = Service("C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\asserts\\127.0.6533.119\\chromedriver.exe")
    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()

    # 返回网页的高度的js代码2
    js_height = "return document.body.clientHeight"
    picname = saveImgName
    print("shotWEB" + name)
    link = name
    try:
        driver.get(link)
        time.sleep(2)
        # driver.delete_all_cookies()
       # driver.refresh()
        driver.get_screenshot_as_file(picname)
        print("Process {} get one pic !!!".format(os.getpid()))
        driver.close()
        return True
    except Exception as e:
        print(picname, e)
        driver.close()
        return False


def webcheck(name):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    service = Service("C:\\Pycharm_projects\\SaYibot\\SaYi\\src\\asserts\\127.0.6533.119\\chromedriver.exe")
    driver = webdriver.Chrome(options=options, service=service)
    driver.maximize_window()
    # 返回网页的高度的js代码
    js_height = "return document.body.clientHeight"
    print("checkWEB" + name)
    link = name
    # driver.get(link)
    try:
        driver.get(link)
        driver.close()
        return True
    except Exception as e:
        print(e)
        driver.close()
        return False
