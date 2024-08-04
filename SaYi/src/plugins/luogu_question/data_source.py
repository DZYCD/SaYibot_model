
from selenium import webdriver
import time
import os.path
from selenium.webdriver.chrome.options import Options

def webshot(ti,saveImgName):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    chromedriver = r"C:\Users\Shuai\AppData\Local\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    # 返回网页的高度的js代码
    js_height = "return document.body.clientHeight"
    picname = saveImgName
    print(f"https://www.luogu.com.cn/problem/{ti}")
    link = f"https://www.luogu.com.cn/problem/{ti}"
    # driver.get(link)
    try:
        driver.get(link)
        driver.delete_all_cookies()
        driver.add_cookie({"name": "_uid", "value": "1092531"})
        driver.add_cookie({"name": "__client_id", "value": "328ff25160515289d33fd841faa5791e043fef5d"})
        driver.refresh()
        k = 1
        height = driver.execute_script(js_height)
        while True:
            if k * 500 < height:
                js_move = "window.scrollTo(0,{})".format(k * 500)
                # print(js_move)
                driver.execute_script(js_move)
                time.sleep(0.2)
                height = driver.execute_script(js_height)
                k += 1
            else:
                break
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(picname)
        print("Process {} get one pic !!!".format(os.getpid()))
    except Exception as e:
        print(picname, e)


