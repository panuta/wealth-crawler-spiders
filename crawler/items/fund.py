import scrapy


class MutualFundItem(scrapy.Item):

    fund_manager = scrapy.Field()
    fund_code = scrapy.Field()
    fund_name_th = scrapy.Field()
    fund_name_en = scrapy.Field()

    nav_date = scrapy.Field()
    nav = scrapy.Field()
    total_nav = scrapy.Field()

    bid_price = scrapy.Field()
    offer_price = scrapy.Field()

    raw = scrapy.Field()

    exclude_from_indexes = (
        'fund_name_th',
        'fund_name_en',
        'nav',
        'total_nav',
        'bid_price',
        'offer_price',
        'raw',
    )