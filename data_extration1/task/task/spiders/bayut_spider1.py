import scrapy
from scrapy.http import response


class BayutSpider(scrapy.Spider):
    name = "bayut"
    page_number = 2
    start_urls = [
        "https://www.bayut.com/to-rent/property/dubai/page-1/"
    ]

    def parse(self, response):
        title = response.xpath('//title/text()').get()


    next_page = "https://www.bayut.com/to-rent/property/dubai/" + str(BayutSpider.page_number) + "/"
    if BayutSpider.page_number >= 50:
        BayutSpider.page_number += 1
        yield response.follow(next_page, callback=parse)

