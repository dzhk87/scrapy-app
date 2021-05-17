import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime
from ..items import QuotesItem
from uuid import uuid4


class DefaultSpider(scrapy.Spider):
    name = 'default'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote_div in response.css('div.quote'):
            l = ItemLoader(item=QuotesItem(), selector=quote_div)
            currenttime = datetime.now().isoformat()
            quoteid = str(uuid4())

            l.add_css('text', 'span.text')
            l.add_css('author', 'small.author')
            l.add_css('tags', 'meta.keywords::attr(content)')
            l.add_value('id', quoteid)
            l.add_value('createdtime', currenttime)
            l.add_value('modifiedtime', currenttime)

            yield l.load_item()

        next_page = response.css('li.next')
        if len(next_page) & len(next_page.css('a')):
            link = next_page.css('a').attrib['href']
            yield response.follow(link, callback=self.parse)
