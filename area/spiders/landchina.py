# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.http import Request
from area.items import *
from area.settings import *
from area.pipelines import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

class LandchinaSpider(scrapy.Spider):
    name = "landchina"
    allowed_domains = ["landchina.com"]
    start_urls = (

        # 'http://www.landchina.com/default.aspx?tabid=263&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&p=9f2c3acd-0256-4da2-a659-6949c4671a2a%3A2015-1-1%7E2015-12-31%7C42ad98ae-c46a-40aa-aacc-c0884036eeaf%3A52%25%7E%u8D35%u5DDE%u7701',
        'http://www.landchina.com/default.aspx?tabid=263&wmguid=75c72564-ffd9-426a-954b-8ac2df0903b7&p=9f2c3acd-0256-4da2-a659-6949c4671a2a%3A2015-1-1%7E2015-12-31%7C42ad98ae-c46a-40aa-aacc-c0884036eeaf%3A3211%25%7E%u9547%u6C5F%u5E02',

    )
    # driver = webdriver.Firefox()
    service_args = ['--load-images=false', '--disk-cache=true']
    driver = webdriver.PhantomJS(executable_path = '/usr/local/bin/phantomjs', service_args = service_args)

    def parse(self, response):
        ori = 'http://www.landchina.com/'
        sel = Selector(response)
        for row in sel.xpath('//tr[@onmouseover]'):
            item = AreaItem()
            path = row.xpath('td/text()').extract()
            item['number'] = path[0]
            # item['distinct'] = path[1]
            # item['location'] = row.xpath('td/a/text()').extract()[0]
            # item['area'] = path[2]
            # item['application'] = path[3]
            # item['way'] = path[4]
            # item['date'] = path[5]
            issue = row.xpath('td/a/@href').extract()[0]
            yield Request(url = ori + issue, callback = lambda response, Items=item : self.parse3(response, Items))

        self.driver.get(response.url)
        num_page = 174
        for it in xrange(1, num_page):
            # yield self.parse2(sel)
            # self.driver.find_element_by_xpath('/a[contains(@onclick="'+ _onclick +'")]').click()
            _onclick = "QueryAction.GoPage(\'TAB\',{0})".format(it+1)
            lu = '//a[contains(@onclick, "'+ _onclick+'")]'
            self.driver.find_element_by_xpath(lu).click()
            sel = Selector(text = self.driver.page_source)
            for row in sel.xpath('//tr[@onmouseover]'):
                item = AreaItem()
                path = row.xpath('td/text()').extract()
                item['number'] = path[0]
                # item['distinct'] = path[1]
                # item['location'] = row.xpath('td/a/text()').extract()[0]
                # item['area'] = path[2]
                # item['application'] = path[3]
                # item['way'] = path[4]
                # item['date'] = path[5]
                issue = row.xpath('td/a/@href').extract()[0]
                yield Request(url = ori + issue, callback = lambda response, Items=item : self.parse3(response, Items), dont_filter = True)
        self.driver.close()

    def parse3(self, response, Items):
        sel = Selector(response)
        Items['location'] = sel.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl"]/text()').extract()[0]
        Items['date'] = sel.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl"]/text()').extract()[0]
        Items['distinct'] = sel.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl"]/text()').extract()[0]
        Items['area'] = sel.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl"]/text()').extract()[0]
        Items['application'] = sel.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl"]/text()').extract()[0]
        Items['way'] = sel.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl"]/text()').extract()[0]

        if len(sel.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl"]/text()').extract()) == 0:
            Items['price'] = u'0'
            # print response.url
        else:
            Items['price'] = sel.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl"]/text()').extract()[0]
        return Items


    def parse2(self, sel):
        ori = 'http://www.landchina.com/'
        # sel = Selector(response)
        for row in sel.xpath('//tr[@onmouseover]'):
            item = AreaItem()
            path = row.xpath('td/text()').extract()
            item['number'] = path[0]
            # item['distinct'] = path[1]
            # item['location'] = row.xpath('td/a/text()').extract()[0]
            # item['area'] = path[2]
            # item['application'] = path[3]
            # item['way'] = path[4]
            # item['date'] = path[5]
            issue = row.xpath('td/a/@href').extract()[0]
            yield Request(url = ori + issue, callback = lambda response, Items=item : self.parse3(response, Items), dont_filter = True)
