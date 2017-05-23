# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    book_name = scrapy.Field()  # 图书名
    book_star = scrapy.Field()  # 图书评分
    book_pl = scrapy.Field()  # 图书评论数
    book_author = scrapy.Field()  # 图书作者
    book_publish = scrapy.Field()  # 出版社
    book_date = scrapy.Field()  # 出版日期
    book_price = scrapy.Field()  # 图书价格

