import json

import scrapy

from crawler.items.sample import SampleItem


class SampleSpider(scrapy.Spider):
    name = 'SampleSpider'
    item_pipelines = {}  # Disabled all pipelines

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
            item = SampleItem()
            item['item_json'] = json.dumps(resource)
            yield item
