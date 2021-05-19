import scrapy


class BayutSpider(scrapy.Spider):
    name = "bayut"
    page_number = 2
    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']

    def parse(self, response):
        itm = response.xpath("//*/div[@class='bbfbe3d2']/ul/"
                             "li[@class='ef447dde']article[@class='ca2f5674']/"
                             "div[@class='_4041eb80']/a[@class='_287661cb']").getall()
        print(itm)
        for ad in response.xpath("//*/div[@class='bbfbe3d2']/ul/li[@class='ef447dde']/div[@class='_4041eb80'] > a[@class='_287661cb'] > a/attr('href')"):
            yield scrapy.Request(url=ad.get(), callback=self.parseInnerPage)


            next_page = "https://www.bayut.com/to-rent/property/dubai/" + str(BayutSpider.page_number) + "/"
            if BayutSpider.page_number is not None:
                BayutSpider.page_number += 1
                yield response.follow(next_page, callback=self.parse)

    def parseInnerPage(self, response):
        yield




