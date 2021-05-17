# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from uuid import uuid4
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapyapp.models import Quote, Author, Tag, QuoteAndTag


class QuotesPipeline:
    def open_spider(self, spider):
        self.file = open('result.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # export to json
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        # save in db
        self.file.write(line)
        authorname = item['author']
        authorid = str(uuid4())

        try:
            author = Author.objects.get(name=authorname)
        except Author.DoesNotExist:
            author = Author.objects.create(id=authorid, name=authorname)

        text = item['text']
        try:
            # assumes that (text, author) is primary key
            quote = Quote.objects.get(text=text, author=author)
            quote = Quote.objects.update(modifiedtime=item['modifiedtime'])
        except Quote.DoesNotExist:
            quote = Quote.objects.create(id=item['id'],
                                         text=text,
                                         author=author,
                                         createdtime=item['createdtime'],
                                         modifiedtime=item['modifiedtime'])

        tags = item['tags']
        for tagname in tags:
            try:
                tag = Tag.objects.get(name=tagname)
            except Tag.DoesNotExist:
                tagid = str(uuid4())
                tag = Tag.objects.create(id=tagid,
                                         name=tagname)
            try:
                QuoteAndTag.objects.get(tag=tag,
                                        quote=quote)
            except QuoteAndTag.DoesNotExist:
                quoteandtagid = str(uuid4())
                QuoteAndTag.objects.create(id=quoteandtagid,
                                           tag=tag,
                                           quote=quote)

        return item
