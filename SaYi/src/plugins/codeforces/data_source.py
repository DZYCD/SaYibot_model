from selenium import webdriver
import time
import os.path
import requests
import hashlib
import random
import json
from ..dataset_controller import DataSetControl

job_path = "C:\\Users\\DZYCD\\PycharmProjects\\SaYibot\\SaYi\\src\\plugins\\time_freezer\\job_list.json"
dataset = DataSetControl(job_path)


def get_dic(website, name=""):
    times = int(time.time())
    rad = random.randint(100000, 999999)
    key = "8f66b2baba19bdfbc841726006a55f0cab51b1e1"
    secret = "cadde93cc6f84429aa0b364feb0fe369eed8c8d7"
    k = "{0}/{1}?apiKey={3}&{2}time={4}#{5}".format(rad, website, name, key, times, secret)
    # print(k)
    # k = str(rad) + "/" + website + "?apikey=" + key + "&time=" + str(times) + "#" + secret
    hash_form = hashlib.sha512()
    hash_form.update(k.encode())
    web = "https://codeforces.com/api/{0}?{1}apiKey={2}&time={3}&apiSig={4}{5}".format(website, name, key, times, rad,
                                                                                    hash_form.hexdigest())
    dic = requests.get(web)
    # print(web)
    return json.loads(dic.text)


def to_date(seconds):
    timeArray = time.localtime(seconds)  # 秒数
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def to_minutes(seconds):
    return str(seconds//60)


def webshot(name, saveImgName):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chromedriver = r"C:\Users\Shuai\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # 返回网页的高度的js代码
    js_height = "return document.body.clientHeight"
    picname = saveImgName
    print(f"https://codeforces.com/profile/{name}")
    link = f"https://codeforces.com/profile/{name}"
    # driver.get(link)
    try:
        driver.get(link)
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
    print(f"https://codeforces.com/profile/{name}")
    link = f"https://codeforces.com/profile/{name}"
    # driver.get(link)
    try:
        driver.get(link)
        driver.close()
        return True
    except Exception as e:
        print(e)
        driver.close()
        return False


def get_contest_hack():
    pass
def get_user_info(name):
    res = get_dic("user.info", "handles="+name+"&")
    try:
        info = res["result"][0]
        info["lastOnlineTimeSeconds"] = to_date(info["lastOnlineTimeSeconds"])
        info["registrationTimeSeconds"] = to_date(info["registrationTimeSeconds"])
        return info
    except:
        return False


def get_contest_list():
    contest = get_dic("contest.list?")
    contest_list = contest["result"]
    trans = {
        "CF": "cf积分赛制",
        "ICPC": "ICPC赛制",
        "IOI": "IOI赛制"
    }
    dataset_list = dataset.get_value("result", "job_list")
    contest_result = []
    for i in contest_list:
        if i["phase"] == "BEFORE":
            info = i["id"], i["name"], trans[i["type"]], to_minutes(i["durationSeconds"]), to_date(
                i["startTimeSeconds"])
            contest_result.append(info)
            flag = 1
            for p in dataset_list:
                if p[0] == i["startTimeSeconds"] and p[1] == "cf_contest_annotation":
                    p[2] = i["name"]
                    flag = 0
            if flag:
                dataset_list.append([i["startTimeSeconds"], "cf_contest_annotation", i["name"]])
        else:
            dataset.update_value("result", "job_list", dataset_list)
            dataset.update_value("result", "job_count", len(dataset_list))
            return contest_result
