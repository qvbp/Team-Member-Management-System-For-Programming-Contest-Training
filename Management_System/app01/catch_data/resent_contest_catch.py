from lxml import etree

import requests

from app01 import models

from celery import Celery

app = Celery('Management_System')


@app.task
def contest_crawl_data():
    # 首先删除表中所有的数据
    models.CFContestInfo.objects.all().delete()
    models.AtCoderContestInfo.objects.all().delete()
    models.NewCodeContestInfo.objects.all().delete()
    # 获取三个OJ近期比赛页面的url
    url_cf = "https://codeforces.com/contests"
    url_atcoder = "https://atcoder.jp/contests/"
    url_newcode = "https://ac.nowcoder.com/acm/contest/vip-index?topCategoryFilter=14"
    # 分别拿到三个页面的源码，并将页面源码编码修改为utf-8
    response_cf = requests.get(url_cf)
    response_atcoder = requests.get(url_atcoder)
    response_newcode = requests.get(url_newcode)
    response_cf.encoding = "utf-8"
    response_atcoder.encoding = "utf-8"
    response_newcode.encoding = "utf-8"
    # 以文本形式获取页面源码
    et_cf = etree.HTML(response_cf.text)
    et_atcoder = etree.HTML(response_atcoder.text)
    et_newcode = etree.HTML(response_newcode.text)

    # CodeForce
    table = et_cf.xpath("//table[@class='']")[0]
    trs = table.xpath("./tr")
    for tr in trs[1:]:
        name = tr.xpath("normalize-space(./td[1]/text())")
        start_date = tr.xpath("normalize-space(./td[3]/a/span/text())")
        duration = tr.xpath("normalize-space(./td[4]/text())")
        models.CFContestInfo.objects.create(name=name, start_time=start_date, duration=duration)
        # print(name, start_date, duration)

    # AtCoder
    trs = et_atcoder.xpath('//*[@id="contest-table-upcoming"]/div/div/table/tbody/tr')
    for tr in trs:
        name = tr.xpath("./td[2]/a/text()")[0]
        start_date = tr.xpath("./td[1]/a/time/text()")[0]
        duration = tr.xpath("./td[3]/text()")[0]
        models.AtCoderContestInfo.objects.create(name=name, start_time=start_date, duration=duration)
        # print(name, start_date, duration)

    # NewCode
    divs = et_newcode.xpath('//div[@class="platform-item js-item "]')
    for div in divs:
        class_data = div.xpath("./@class")
        if class_data and class_data[0] == "platform-mod-hd clearfix":
            continue

        name = div.xpath("normalize-space(./div[2]/div[1]/h4/a/text())")
        registration_time = div.xpath("normalize-space(./div[2]/div[1]/ul/li[1]/text())")[6:]
        start_date = div.xpath("normalize-space(./div[2]/div[1]/ul/li[2]/text())")[6:41]
        duration = div.xpath("normalize-space(./div[2]/div[1]/ul/li[2]/text())")[46:49]
        models.NewCodeContestInfo.objects.create(name=name, registration_time=registration_time, start_time=start_date,
                                                 duration=duration)
        # print(f'{name}\n{registration_time}\n{start_date}\n{duration}\n')
