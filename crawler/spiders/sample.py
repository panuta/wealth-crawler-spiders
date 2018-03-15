import json
import uuid

import scrapy

from crawler.items.sample import SampleItem


class SampleSpider(scrapy.Spider):
    name = 'SampleSpider'

    def start_requests(self):
        yield scrapy.Request(
            url='https://jsonplaceholder.typicode.com/posts',
            callback=self.parse,
        )

    def parse(self, response):
        if not response or not response.body_as_unicode():
            return

        response_json = json.loads(response.body_as_unicode())

        for resource in response_json:
            item = SampleItem(str(uuid.uuid4()))
            item['item_json'] = json.dumps(resource)
            yield item
