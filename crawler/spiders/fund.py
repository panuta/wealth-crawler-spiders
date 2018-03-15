import csv
from datetime import date, timedelta

import scrapy

from crawler.items.fund import MutualFundItem


class MutualFundSpider(scrapy.Spider):
    name = 'MutualFundSpider'

    def start_requests(self):
        # https://www.thaimutualfund.com/AIMC/aimc_navCenterDownloadRepRep.jsp?date=13/03/2561
        yesterday = date.today() + timedelta(days=-1)

        yield scrapy.Request(
            url='https://www.thaimutualfund.com/AIMC/aimc_navCenterDownloadRepRep.jsp?date={}'.format(
                '{day}/{month}/{year}'.format(day=yesterday.day, month=yesterday.month, year=yesterday.year + 543)
            ),
            callback=self.parse,
            meta={
                'date': yesterday,
            }
        )

    def parse(self, response):
        response_body_as_unicode = response.body.decode('cp874')

        for response_line in response_body_as_unicode.splitlines():
            if not response_line:
                continue

            item = MutualFundItem()
            item['raw'] = response_line

            response_csv = None
            for _ in csv.reader([response_line]):
                response_csv = _

            if not response_csv:
                continue

            item['nav_date'] = response.meta['date']
            item['fund_manager'] = response_csv[2]
            item['fund_code'] = response_csv[6]
            item['fund_name_th'] = response_csv[4]
            item['fund_name_en'] = response_csv[5]
            item['nav'] = response_csv[8]
            item['total_nav'] = response_csv[7]
            item['offer_price'] = response_csv[11]
            item['bid_price'] = response_csv[12]

            yield item
