from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from douban.items import DoubanItem
import scrapy


class DoubanSpiderSpider(BaseSpider):
    name = "douban_spider"
    allowed_domains = ["book.douban.com"]
    start_urls = (
        'https://book.douban.com/tag/%E5%8E%86%E5%8F%B2',
        )

    def parse(self, response):
        sel = Selector(response)
        booklist = sel.css('#subject_list > ul > li')
        for book in booklist:
            item = DoubanItem()
            try:
                # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
                item['book_name'] = book.xpath('div[@class="info"]/h2/a/text()').extract()[0].strip()
                item['book_star'] = book.xpath("div[@class='info']/div[2]/span[@class='rating_nums']/text()").extract()[
                    0].strip()
                item['book_pl'] = book.xpath("div[@class='info']/div[2]/span[@class='pl']/text()").extract()[0].strip()
                pub = book.xpath('div[@class="info"]/div[@class="pub"]/text()').extract()[0].strip().split('/')
                item['book_price'] = pub.pop()
                item['book_date'] = pub.pop()
                item['book_publish'] = pub.pop()
                item['book_author'] = '/'.join(pub)
                yield item
            except:
                pass
        nextPage = sel.xpath('//div[@id="subject_list"]/div[@class="paginator"]/span[@class="next"]/a/@href').extract()[
            0].strip()
        if nextPage:
            next_url = 'https://book.douban.com' + nextPage
            yield scrapy.http.Request(next_url, callback=self.parse)


