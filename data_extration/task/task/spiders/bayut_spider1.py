import scrapy
import time
import json
from pydispatch import dispatcher
from scrapy import signals


class BayutSpider(scrapy.Spider):
    name = "bayut"
    allowed_domains = ['bayut.com']
    # page_number = 2
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']
    counter = 0
    results = {}


    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        # itm = response.xpath("//*/article/div[1]/a/@href").getall()
        for ad in response.xpath("//*/article/div[1]/a/@href"):
            time.sleep(3)
            yield scrapy.Request(url=response.urljoin(ad.get()), callback=self.parseInnerPage)

            next_page = response.xpath("//*/main/div[3]/div[3]/div[2]/div[1]/div[2]/ul/li[*]/a/@href").get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)


    def parseInnerPage(self, response):
        property_id = response.xpath("//*/main/div[1]/div/div/span/text()").get()
        purpose = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[2]/ul/li[2]/span[2]/text()").get()
        type = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[2]/ul/li[1]/span[2]/text()").get()
        added_on = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[2]/ul/li[6]/span[2]/text()").get()
        furnishing = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[2]/ul/li[4]/span[2]/text()").get()
        priceDict = {}
        currency_sym = response.xpath("//*/main/div[3]/div[1]/div[2]/div[1]/div[1]/div/span[1]/text()").get()
        amount_amt = response.xpath("//*/main/div[3]/div[1]/div[2]/div[1]/div[1]/div/span[3]/text()").get()
        priceDict['currency'] = currency_sym
        priceDict['amount'] = amount_amt
        location = response.xpath("//*/main/div[3]/div[1]/div[2]/div[2]/text()").get()
        bbsDict = {}
        bedrooms = response.xpath("//*/main/div[3]/div[1]/div[2]/div[3]/div[1]/span[2]/span/text()").get()
        bathrooms = response.xpath("//*/main/div[3]/div[1]/div[2]/div[3]/div[2]/span[2]/span/text()").get()
        bedrooms = bedrooms.replace("Beds", "")
        bathrooms = bathrooms.replace("Baths", "")
        size = response.xpath("//*/main/div[3]/div[1]/div[2]/div[3]/div[3]/span[2]/span/span/text()").get()
        bbsDict['bedrooms'] = bedrooms
        bbsDict['bathrooms'] = bathrooms
        bbsDict['size'] = size
        permit_number= response.xpath("//*/main/div[3]/div[2]/div[1]/div[1]/div/div[2]/span[3]/text()[3]").get()
        agent_name = response.xpath("//*/main/div[3]/div[2]/div[1]/div[1]/div/div[3]/span[2]/text()").get()
        image_url = response.xpath("//*/main/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/picture/source/@srcset").get()
        breadcrumbs1 = response.xpath("//*/main/div[1]/div/div/a[2]/span/text()").get()
        breadcrumbs2 = response.xpath("//*/main/div[1]/div/div/a[3]/span/text()").get()
        breadcrumbs3 = response.xpath("//*/main/div[1]/div/div/a[4]/span/text()").get()
        breadcrumbs = breadcrumbs1 + breadcrumbs2 + breadcrumbs3
        f1=[]
        ame = response.xpath("//*/main/div[3]/div[1]/div[6]/div/div/div[*]/div[2]/span/text()").getall()
        if ame is not None:
            f1.append(ame)
        description = response.xpath("//*/main/div[3]/div[1]/div[4]/div/div[1]/div[1]/div/div/div/span/text()").getall()
        if permit_number is not None:
            print(permit_number)
        if agent_name is not None:
            print(agent_name)

        time.sleep(3)


        self.results[self.counter] = {

            'property_id' : property_id,
            'purpose' : purpose,
            'type' : type,
            'added_on' : added_on,
            'furnishing' : furnishing,
            'price' : priceDict,
            'permit_number': permit_number,
            'agent_name' : agent_name,
            'location' : location,
            'bed_bath_size' : bbsDict,
            'image_url' : image_url,
            'breadcrumbs' : breadcrumbs,
            'amenities' : f1,
            'description ' : description

        }
        self.counter = self.counter+1

    def spider_closed(self, spider):
        with open('bayut1.json', 'w') as fp:
            json.dump(self.results, fp)

