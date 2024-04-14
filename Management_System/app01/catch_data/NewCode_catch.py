from lxml import etree

import requests

from app01 import models

from celery import Celery

app = Celery('Management_System')


@app.task
def NewCode_crawl_data():
    id_list = models.NewCodeInfo.objects.values_list('NewCoder_num', flat=True)
    for id in id_list:
        if id == "Null":
            continue
        url1 = f"https://ac.nowcoder.com/acm/contest/profile/{id}"  # 拿rating
        url2 = f"https://ac.nowcoder.com/acm/contest/profile/{id}/practice-coding"  # 拿做题数
        response1 = requests.get(url1)
        response2 = requests.get(url2)
        response1.encoding = "utf-8"
        response2.encoding = "utf-8"
        et1 = etree.HTML(response1.text)
        et2 = etree.HTML(response2.text)
        try:
            # 拿名字
            name = et1.xpath("/html/body/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/a[1]/text()")[0]
            # 拿分数和排名
            rank = et1.xpath("/html/body/div/div[2]/div[2]/section/div[1]/div[2]/div/text()")[0]
            rating = et1.xpath('/html/body/div/div[2]/div[2]/section/div[1]/div[1]/div/text()')[0]
            # 拿做题数
            solved_num = et2.xpath('/html/body/div[1]/div[2]/div[2]/section/div[1]/div[2]/div/text()')[0]
            # 对数据做判断
            if rank == "暂无":
                rank = "0"
            if rating == "暂无":
                rating = "0"
            if solved_num == "暂无":
                solved_num = "0"
            models.NewCodeInfo.objects.filter(NewCoder_num=id).update(NewCoder_id=name, rating=rating, rank=rank,
                                                                      solved=solved_num)
        except IndexError:
            # 如果出现IndexError异常，则跳过当前循环，继续执行下一个循环
            continue
