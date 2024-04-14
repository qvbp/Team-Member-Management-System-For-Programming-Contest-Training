
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import requests

from app01 import models

from celery import Celery

app = Celery('Management_System')


@app.task
def cf_crawl_data():

    id_list = models.CfInfo.objects.values_list('CodeForce_id', flat=True)
    for id in id_list:
        if id == "Null":
            continue
        url = f"https://codeforces.com/profile/{id}"
        response = requests.get(url)
        response.raise_for_status()  # 如果请求不成功，会抛出异常
        response.encoding = "utf-8"

        page = BeautifulSoup(response.text, 'html.parser')

        span_list = page.find_all("span", attrs={"style": "font-weight:bold;"})
        div_list = page.find_all("div", attrs={"class": "_UserActivityFrame_counterValue"})
        all_exercise = ""
        year_exercise = ""
        month_exercise = ""
        for i in range(3):
            st = 0
            ed = 0
            s = div_list[i].text
            for index in range(len(s)):
                if s[index] == " ":
                    ed = index
                    break
            if i == 0:
                all_exercise = s[st:ed]
            elif i == 1:
                year_exercise = s[st:ed]
            else:
                month_exercise = s[st:ed]
        rating = span_list[0].text
        top_rating = span_list[2].text
        models.CfInfo.objects.filter(CodeForce_id=id).update(rating=rating, max_rating=top_rating,
                                     solved_all_time=all_exercise, solved_last_month=month_exercise,
                                     solved_last_year=year_exercise)