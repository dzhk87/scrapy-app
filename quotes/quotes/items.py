# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from itemloaders.processors import Compose, TakeFirst, MapCompose
from w3lib.html import remove_tags
from scrapyapp.models import Quote


def format_tags(tags):
    return list(filter(None, tags.pop().split(',')))


def take_first(arr):
    return arr.pop()


class QuotesItem(DjangoItem):
    django_model = Quote
    id = scrapy.Field(output_processor=TakeFirst())
    text = scrapy.Field(input_processor=MapCompose(remove_tags),
                        output_processor=TakeFirst())
    author = scrapy.Field(input_processor=MapCompose(remove_tags),
                          output_processor=TakeFirst())
    tags = scrapy.Field(input_processor=MapCompose(remove_tags),
                        output_processor=Compose(format_tags))
    createdtime = scrapy.Field(output_processor=Compose(take_first))
    modifiedtime = scrapy.Field(output_processor=Compose(take_first))
