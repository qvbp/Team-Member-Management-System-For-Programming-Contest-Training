import os
import urllib.request as requestd
from time import sleep
from app01 import models
from celery import Celery
from PIL import Image
import io

import ddddocr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options

app = Celery('Management_System')
@app.task
def LuoGu_crawl_data():
    # 实例化解析验证码图片类
    ocr = ddddocr.DdddOcr()

    # 解析验证码图片
    def get_captcha(img_bytes):
        captcha = ocr.classification(img_bytes)
        return captcha

    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument('--disable-gpu')
    opt.add_argument('--start-maximized')
    web = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opt)
    web.implicitly_wait(10)

    web.get("https://www.luogu.com.cn/auth/login")
    web.implicitly_wait(10)

    max_attempts = 20  # 最大尝试次数
    attempts = 0
    flag = True

    while attempts < max_attempts:
        img_url = web.find_element(by=By.XPATH,
                                   value='//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[3]/div/div[2]/img')
        png_code_img = img_url.screenshot_as_png
        web.implicitly_wait(10)
        image = Image.open(io.BytesIO(png_code_img))
        captcha = get_captcha(image)

        # web.find_element(by=By.XPATH,
        #                  value='//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[1]/div/input').clear()
        # web.find_element(by=By.XPATH,
        #                  value='//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[2]/div/input').clear()
        # web.find_element(by=By.XPATH,
        #                  value='//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[3]/div/div[1]/input').clear()
        if flag:
            web.find_element(by=By.XPATH,
                             value='//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[1]/div/input').send_keys(
                "15622163461")
            web.find_element(by=By.XPATH,
                             value='//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[2]/div/input').send_keys(
                "s13533980154csw")
            flag = False
        web.find_element(by=By.XPATH,
                         value='//*[@id="app"]/div[2]/main/div/div/div/div/div/div/div[3]/div/div[1]/input').send_keys(
            captcha)
        web.find_element(by=By.XPATH,
                         value='//*[@id="app"]/div[2]/main/div/div/div/div/div/div/button').click()
        web.implicitly_wait(10)

        try:
            web.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[3]/button[1]')
            print("验证码不正确，尝试重新登录")
            error = web.find_element(by=By.XPATH, value='/html/body/div[2]/div/div[3]/button[1]')
            error.click()
            attempts += 1
            sleep(2)
        except NoSuchElementException:
            print("登录成功")
            break

    if attempts == max_attempts:
        print("达到最大尝试次数，登录失败")

    # 爬取数据
    id_list = models.LuoGuInfo.objects.values_list('LuoGu_num', flat=True)
    for id in id_list:
        if id == "Null":
            continue
        web.get(f"https://www.luogu.com.cn/user/{id}")
        web.implicitly_wait(10)
        name = web.find_element(by=By.XPATH,
                                value='//*[@id="app"]/div[2]/main/div/div[1]/div[1]/div[1]/div[1]/span')
        solved = web.find_element(by=By.XPATH,
                                      value='//*[@id="app"]/div[2]/main/div/div[1]/div[2]/div[2]/div/div[4]/a/span[2]')
        rating = web.find_element(by=By.XPATH,
                                        value='//*[@id="app"]/div[2]/main/div/div[1]/div[2]/div[2]/div/div[5]/div/span[2]')

        solved = solved.text.strip()
        rating = rating.text.strip()
        name = name.text.strip()

        # 判断一下数据是否为空
        if solved == "0" or solved == "-":
            solved = "0"
        if rating == "-":
            rating = "Null"

        models.LuoGuInfo.objects.filter(LuoGu_num=id).update(LuoGu_id=name, solved=int(solved), rating=rating)

        # print(solved.text, rating.text)
    web.quit()
