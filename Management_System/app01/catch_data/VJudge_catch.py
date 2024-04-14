
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import requests

from app01 import models

from celery import Celery

app = Celery('Management_System')


@app.task
def VJudge_crawl_data():
    id_list = models.VJudgeInfo.objects.values_list('VJudge_id', flat=True)
    for id in id_list:
        if id == "Null":
            continue
        url = f"https://vjudge.net/user/{id}"
        response = requests.get(url)
        response.encoding = "utf-8"

        page = BeautifulSoup(response.text, 'html.parser')

        a_list = page.find_all("a", {"target": "_blank"})
        last_24hours_solved = a_list[0].text
        last_7days_solved = a_list[1].text
        last_30days_solved = a_list[2].text
        overall_solved = a_list[3].text
        models.VJudgeInfo.objects.filter(VJudge_id=id).update(Overall_solved=overall_solved, last_24hours_solved=last_24hours_solved,
                                     last_7days_solved=last_7days_solved, last_30days_solved=last_30days_solved)
