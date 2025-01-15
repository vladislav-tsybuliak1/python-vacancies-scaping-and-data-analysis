# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Vacancy(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    exp_level = scrapy.Field()
    company = scrapy.Field()
    placing_date = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
