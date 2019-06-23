#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'chenquanbin'
# __date__ = '2019-06-22'

import scrapy
import re
from Court.items import LawyerItem
DUBUG_MODE = 1

class CourtSpider(scrapy.Spider):
    name = "Court"
    allowed_domains = ["fabang.com"]
    start_urls = ["http://lawyer.fabang.com/list/" + str(placeholder * 500) + "-0-0-key-1-1.html" for placeholder in range(1,32)]

    if DUBUG_MODE:
        start_urls = ['http://lawyer.fabang.com/list/500-0-0-key-1-1.html']

    def parse(self, response):
        sel = response.xpath('//ul[@id="category-sub-list"]')[0]
        for sel1 in sel.xpath('li'):
            next_url = 'http://lawyer.fabang.com/list/'+ sel1.xpath('a/@href').extract()[0]
            yield scrapy.Request(next_url, self.parse2)

    def parse2(self,response):
        city = response.xpath("//a[@class='current']/text()").extract()[1].strip()
        province = response.xpath("//a[@class='current']/text()").extract()[0].strip()

        for lawyerlist in response.css(".lawyerarea"):
            uname = lawyerlist.xpath('div[1]/div[1]/a[@class="uname"]/text()').extract()[0]

            if len(lawyerlist.xpath("div[2]/a")):
                office = lawyerlist.xpath("div[2]/a/text()").extract()[0]
            else:
                office = lawyerlist.xpath("div[2]").extract()[0]
                office = re.sub(r".*\n.*an>","", office, re.S)
                office = re.sub(r"\s*</div>","",office, re.I).strip()
            phone = lawyerlist.xpath('div[5]/div[2]/text()').extract()[0]

            # print(uname, office, phone)
            lawyer = LawyerItem()
            lawyer['name'] = uname
            lawyer['office'] = office
            lawyer['phone'] = phone
            lawyer['city'] = city
            lawyer['province'] = province

            yield lawyer

        #抓取末页页码
        last_page_url = "http://lawyer.fabang.com/list/"+ response.xpath("//a[contains(text(),'末页')]/@href").extract()[0]
        last_page_num = int(re.search(r'.*-(.*).html',last_page_url).group(1))
        current_page_num = int(re.search(r'.*-(.*).html',response.url).group(1))

        # request for next page
        if current_page_num < last_page_num:
            next_page_num = current_page_num + 1
            next_page_url = re.sub(r'-\d+\.html','-'+ str(next_page_num) + '.html', response.url)
            yield scrapy.Request(next_page_url, self.parse2)





