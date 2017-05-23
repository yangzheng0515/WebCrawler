# -*- coding: utf-8 -*-
import scrapy
from xici.items import XiciItem


class XiciSpiderSpider(scrapy.Spider):
    name = "xici_spider"
    allowed_domains = ["www.xicidaili.com"]
    start_urls = ['http://www.xicidaili.com/nn/']
    home_url = 'http://www.xicidaili.com/nn/{page}'

    def start_requests(self):
        for i in range(1, 225):
            yield scrapy.Request(self.home_url.format(page=str(i)), self.parse)

    def parse(self, response):
        item = XiciItem()
        ip_list = response.xpath("//table[@id='ip_list']/tr")

        for tr in ip_list[1:]:
            try:
                item['ip'] = tr.xpath("td[2]/text()")[0].extract()
                item['port'] = tr.xpath("td[3]/text()")[0].extract()
                item['position'] = tr.xpath("td[4]/a/text()")[0].extract()
                item['type'] = tr.xpath("td[6]/text()")[0].extract()
                item['speed'] = tr.xpath("td[7]/div/@title")[0].extract()
                item['last_check_time'] = tr.xpath("td[10]/text()")[0].extract()
            except:
                pass
            yield item


