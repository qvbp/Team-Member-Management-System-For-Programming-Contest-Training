from lxml import etree

import requests

from app01 import models

from celery import Celery

app = Celery('Management_System')


@app.task
def AtCoder_crawl_data():
    id_list = models.AtCoderInfo.objects.values_list('AtCoder_id', flat=True)
    for id in id_list:
        if id == "Null":
            continue
        url = f"https://atcoder.jp/users/{id}"
        response = requests.get(url)
        response.encoding = "utf-8"

        et = etree.HTML(response.text)

        try:
            rank = et.xpath("/html/body/div[1]/div/div[1]/div[3]/table/tr[1]/td/text()")[0]
            rating = et.xpath("/html/body/div[1]/div/div[1]/div[3]/table/tr[2]/td/span[1]/text()")[0]
            top_rating = et.xpath("/html/body/div[1]/div/div[1]/div[3]/table/tr[3]/td/span[1]/text()")[0]
            Rated_Matches = et.xpath("/html/body/div[1]/div/div[1]/div[3]/table/tr[4]/td/text()")[0]
            Last_Competed = et.xpath("/html/body/div[1]/div/div[1]/div[3]/table/tr[5]/td/text()")[0]

            models.AtCoderInfo.objects.filter(AtCoder_id=id).update(rank=rank, rating=rating, max_rating=top_rating,
                                                                    Rated_Matches=Rated_Matches,
                                                                    Last_Competed=Last_Competed)
        except IndexError:
            # 如果出现IndexError异常，则跳过当前循环，继续执行下一个循环
            continue
