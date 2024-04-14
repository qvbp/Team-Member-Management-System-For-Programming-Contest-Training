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


class NewCoderContest(object):
    def __init__(self, contest_id):
        # contest_id 是传入比赛的编号
        self.contest_id = contest_id

    def get_contest_info(self):
        opt = Options()
        opt.add_argument("--headless")
        opt.add_argument('--disable-gpu')
        opt.add_argument('--start-maximized')
        # opt.add_argument('--window-size=1920,1080')  # 设置窗口大小为 1920x1080，根据需要进行调整

        # 打开浏览器窗口
        web = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=opt)
        # 设置隐性等待时间，在需要的元素还没有出现时，等待10秒
        web.implicitly_wait(10)
        try:
            web.get(f'https://ac.nowcoder.com/acm/contest/{self.contest_id}#rank')
            web.implicitly_wait(10)
            sleep(2)
            web.find_element(by=By.XPATH, value='//*[@id="jsCpn_3_component_0"]/input').send_keys("广东外语外贸大学",
                                                                                                  Keys.ENTER)
            web.implicitly_wait(10)
            sleep(2)
            # 比赛名字
            contest_name = web.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div/h1/span[1]').text.strip()
            alltime = web.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div/p[1]/span[1]').text.strip()
            # 比赛开始时间
            start_time = alltime[0:19]
            # 比赛结束时间
            end_time = alltime[22:41]
            # 创建比赛
            # 先判断是否存在
            exists_nc = models.NewCodeContest.objects.filter(num=self.contest_id).exists()
            exists_nc_vj = models.NC_VJ_Contest.objects.filter(num=self.contest_id).exists()
            if not exists_nc:
                contest = models.NewCodeContest.objects.create(name=contest_name, num=self.contest_id, start_date=start_time,
                                                 end_date=end_time)
            if not exists_nc_vj:
                contestx = models.NC_VJ_Contest.objects.create(name=contest_name, num=self.contest_id, start_date=start_time
                                                           , end_date=end_time)

            # # 滚动到页面底部，触发动态加载
            # web.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # sleep(2)  # 等待加载完成
            tr_list = web.find_elements(by=By.XPATH,
                                        value='/html/body/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/table/tbody/tr')
            cnt = 0
            for tr in tr_list:
                # 队伍名字或者是队员的名字
                # /html/body/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[2]/a/span
                # cnt += 1
                NewCode_id = tr.find_element(by=By.XPATH, value='./td[2]/a/span').text.strip()
                exists = models.NewCodeInfo.objects.filter(NewCoder_id=NewCode_id).exists()
                if exists:
                    NewCode_id = models.NewCodeInfo.objects.filter(NewCoder_id=NewCode_id).first().name.name
                # 解题数
                # /html/body/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[4]/span
                solved = tr.find_element(by=By.XPATH, value='./td[4]/span').text.strip()
                # 这里要注意一下ak的情况，会有一个标志在前面
                for i in range(len(solved)):
                    if not '0' <= solved[i] <= '9':
                        solved = solved[0:i]
                        break
                # 罚时
                # /html/body/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[5]/p
                # 注意一个事情，如果用户没出题，那么他的罚时是0
                if solved == '0':
                    time = "0"
                else:
                    time = tr.find_element(by=By.XPATH, value='./td[5]/p').text.strip()

                # print(f'{cnt}       {NewCode_id}     {solved}     {time}')  # 调试语句

                # 创建队伍数据
                if not exists_nc:
                    models.NewCodeContestData.objects.create(newCodeContest=contest, name=NewCode_id, solved=solved, time=time)
                if not exists_nc_vj:
                    models.NC_VJ_ContestData.objects.create(nC_VJ_Contest=contestx, name=NewCode_id, solved=solved, time=time)
            return "添加成功!"
        except Exception:
            models.NewCodeContest.objects.filter(num=self.contest_id).delete()
            models.NC_VJ_ContestData.objects.filter(num=self.contest_id).delete()
            return "添加失败!"
        finally:
            web.quit()

