from selenium import webdriver
import time
import os.path
import requests
import hashlib
import random
import json
from ..dataset_controller import DataSetControl


def webshot(name, saveImgName):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chromedriver = r"C:\Users\Shuai\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # 返回网页的高度的js代码2
    js_height = "return document.body.clientHeight"
    picname = saveImgName
    print("shotWEB" + name)
    link = name
    try:
        driver.get(link)
        # driver.delete_all_cookies()
        # driver.add_cookie({"name": "_uid", "value": "1092531"})
        # driver.add_cookie({"name": "__client_id", "value": "328ff25160515289d33fd841faa5791e043fef5d"})
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
    chromedriver = r"C:\Users\Shuai\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(options=options)
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
