import scrapy
from scrapy.selector import Selector
import time
import json
import self as self
from scrapy.loader import ItemLoader


class BayutSpider(scrapy.Spider):
    name = "bayut"
    allowed_domains = ['bayut.com']
    # page_number = 2
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']

    def parse(self, response):
        # itm = response.xpath("//*/article/div[1]/a/@href").getall()
        for ad in response.xpath("//*/article/div[1]/a/@href"):
            time.sleep(3)
            yield scrapy.Request(url=response.urljoin(ad.get()), callback=self.parseInnerPage)


            next_page = response.xpath("//*/main/div[2]/div[3]/div[2]/div[1]/div[2]/ul/li[6]/a/@href").get()
            if next_page is not None:
                response.follow(next_page, callback=self.parse)

    def parseInnerPage(self, response):
        property_id = response.xpath("//*/main/div[1]/div/div/span/text()").get()
        purpose = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[2]/ul/li[2]/span[2]/text()").get()
        type = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[2]/ul/li[1]/span[2]/text()").get()
        added_on = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[2]/ul/li[6]/span[2]/text()").get()
        furnishing = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[2]/ul/li[4]/span[2]/text()").get()
        currency = response.xpath("//*/main/div[3]/div[1]/div[2]/div[1]/div[1]/div/span[1]/text()").get()
        amount = response.xpath("//*/main/div[3]/div[1]/div[2]/div[1]/div[1]/div/span[3]/text()").get()
        location = response.xpath("//*/main/div[3]/div[1]/div[2]/div[2]/text()").get()
        bedrooms = response.xpath("//*/main/div[3]/div[1]/div[2]/div[3]/div[1]/span[2]/span/text()").get()
        bathrooms = response.xpath("//*/main/div[3]/div[1]/div[2]/div[3]/div[2]/span[2]/span/text()").get()
        size = response.xpath("//*/main/div[3]/div[1]/div[2]/div[3]/div[3]/span[2]/span/span/text()").get()
        permit_number = response.xpath("//*/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/span[3]/text()[3]").get()
        agent_name = response.xpath("//*/main/div[3]/div[2]/div[1]/div[1]/div/div[3]/span[2]/text()").get()
        image_url = response.xpath("//*/main/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/picture/source/@srcset").get()
        breadcrumbs1 = response.xpath("//*/main/div[1]/div/div/a[2]/span/text()").get()
        breadcrumbs2 = response.xpath("//*/main/div[1]/div/div/a[3]/span/text()").get()
        breadcrumbs3 = response.xpath("//*/main/div[1]/div/div/a[4]/span/text()").get()
        description = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[1]/div[1]/div/div/div/span/text()").getall()
        print(property_id,'*', purpose,'*', type,'*', added_on, '*', furnishing,'*', currency,'*', amount,'*', location)
        time.sleep(3)
        print('*', bedrooms,'*', bathrooms,'*', size,'*', permit_number,'*', agent_name,'*', image_url,'*', breadcrumbs1)
        time.sleep(3)
        print(breadcrumbs2, breadcrumbs3,'*', description)
