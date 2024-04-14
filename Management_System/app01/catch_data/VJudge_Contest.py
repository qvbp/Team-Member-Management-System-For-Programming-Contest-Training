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
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options


class VJudgeContest(object):
    def __init__(self, contest_id):
        # contest_id 是传入比赛的编号
        self.contest_id = contest_id

    def get_contest_info(self):
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument('--disable-gpu')
        # opt.add_argument('--start-maximized')
        opt.add_argument('--window-size=1920,1080')  # 设置窗口大小为 1920x1080，根据需要进行调整

        # 打开浏览器窗口
        web = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opt)
        # 设置隐性等待时间，在需要的元素还没有出现时，等待10秒
        web.implicitly_wait(10)
        try:
            web.get(f'https://vjudge.net/contest/{self.contest_id}#rank')
            web.implicitly_wait(10)
            sleep(2)
            if web.find_element(by=By.XPATH, value='/html/body/div[1]/div/div[2]/div[1]').text == f"No contest {self.contest_id}":
                raise NoSuchElementException()
            login_btn = web.find_element(by=By.XPATH, value='//*[@id="navbarResponsive"]/ul/li[9]/a')
            login_btn.click()
            web.implicitly_wait(10)
            web.find_element(by=By.XPATH, value='//*[@id="login-username"]').send_keys("akccccc")  # 模拟输入用户名
            web.implicitly_wait(10)
            web.find_element(by=By.XPATH, value='//*[@id="login-password"]').send_keys("s13533980154csw")  # 模拟输入密码
            web.implicitly_wait(10)
            yes = web.find_element(by=By.XPATH, value='//*[@id="btn-login"]')  # 模拟点击确认登录
            yes.click()
            web.implicitly_wait(10)
            sleep(2)
            # 以下的密码输入是对上面的更新和优化，先检查是否要输入比赛密码，如若不需要输入则直接跳过
            try:
                web.find_element(by=By.XPATH, value='//*[@id="contest-login-password"]')
                web.find_element(by=By.XPATH, value='//*[@id="contest-login-password"]').send_keys("gdufsacm")
                ok = web.find_element(by=By.XPATH, value='//*[@id="btn-contest-login"]')
                ok.click()
                print("输入密码成功，进入比赛")
            except NoSuchElementException:
                print("不用输入密码，进入比赛成功")
            sleep(2)

            # 把历史的rank关掉
            setting = web.find_element(by=By.XPATH, value='//*[@id="btn-setting"]')
            setting.click()
            try:
                web.find_element(by=By.XPATH, value='//*[@id="setting-check-all"]')
                web.find_element(by=By.XPATH, value='//*[@id="setting-check-all"]').click()
                web.find_element(by=By.XPATH, value='//*[@id="contestSettingModal"]/div/div/div[1]/button').click()
                print("已关闭历史榜单，放心爬取")
            except NoSuchElementException:
                print("没有历史榜单，放心爬取")
            except ElementNotInteractableException:
                print("没有历史榜单，放心爬取")
            sleep(2)

            # 比赛名字
            contest_name = web.find_element(by=By.XPATH, value='//*[@id="time-info"]/div[1]/div[2]/h3').text.strip()
            # 比赛开始时间
            start_time = web.find_element(by=By.XPATH, value='//*[@id="time-info"]/div[1]/div[1]/span').text.strip()[0:16]
            # 比赛结束时间
            end_time = web.find_element(by=By.XPATH, value='//*[@id="time-info"]/div[1]/div[3]/span').text.strip()[0:16]
            # 创建比赛
            # 先判断是否存在
            exists_vj = models.VJudgeContest.objects.filter(num=self.contest_id).exists()
            exists_nc_vj = models.NC_VJ_Contest.objects.filter(num=self.contest_id).exists()
            # print(exists_vj)
            # print(exists_nc_vj)
            if not exists_vj:
                contest = models.VJudgeContest.objects.create(name=contest_name, num=self.contest_id, start_date=start_time,
                                                           end_date=end_time)
            if not exists_nc_vj:
                contestx = models.NC_VJ_Contest.objects.create(name=contest_name, num=self.contest_id, start_date=start_time,
                                                          end_date=end_time)
            # # 滚动到页面底部，触发动态加载
            # web.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # sleep(2)  # 等待加载完成
            tr_list = web.find_elements(by=By.XPATH, value='//*[@id="contest-rank-table"]/tbody/tr')
            # cnt = 0
            for tr in tr_list:
                # cnt += 1
                # 队员的名字
                # //*[@id="contest-rank-table"]/tbody/tr[1]/td[2]/div/a
                VJudge_id = tr.find_element(by=By.XPATH, value='./td[2]/div/a').text.strip()
                for i in range(len(VJudge_id)):
                    if VJudge_id[i] == ' ':
                        VJudge_id = VJudge_id[0:i]
                        break
                exists = models.VJudgeInfo.objects.filter(VJudge_id=VJudge_id).exists()
                if exists:
                    VJudge_id = models.VJudgeInfo.objects.filter(VJudge_id=VJudge_id).first().name.name
                # 解题数
                # //*[@id="contest-rank-table"]/tbody/tr[1]/td[3]/span
                solved = tr.find_element(by=By.XPATH, value='./td[3]/span').text.strip()
                # 罚时
                # //*[@id="contest-rank-table"]/tbody/tr[1]/td[4]/span[1]
                time = tr.find_element(by=By.XPATH, value='./td[4]/span[1]').text.strip()
                # 创建队伍数据
                if not exists_vj:
                    models.VJudgeContestData.objects.create(vJudgeContest=contest, name=VJudge_id, solved=solved, time=time)
                if not exists_nc_vj:
                    models.NC_VJ_ContestData.objects.create(nC_VJ_Contest=contestx, name=VJudge_id, solved=solved, time=time)

                # print(cnt)
            return "添加成功!"
        except Exception:
            models.VJudgeContest.objects.filter(num=self.contest_id).delete()
            models.NC_VJ_Contest.objects.filter(num=self.contest_id).delete()
            return "添加失败!"
        finally:
            web.quit()
