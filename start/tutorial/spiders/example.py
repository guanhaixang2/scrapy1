# -*- coding: utf-8 -*-
import scrapy
import json

from tutorial.items import NikelItem

class ExampleSpider(scrapy.Spider):
    name = 'learn'
    allowed_domains = ['www.nike.com', 'm.nike.com', 'api.nike.com']
    # start_urls = [
    #         'https://www.nike.com/cn/launch/?s=in-stock',
    #         'https://api.nike.com/product_feed/threads/v2/?anchor=50&count=50&filter=marketplace(CN)&filter=language(zh-Hans)&filter=inStock(true)&filter=productInfo.merchPrice.discounted(false)&filter=channelId(010794e5-35fe-4e32-aaff-cd2c74f89d61)&filter=exclusiveAccess(true,false)&fields=active&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.nodes&fields=publishedContent.properties.coverCard&fields=publishedContent.properties.productCard&fields=publishedContent.properties.products&fields=publishedContent.properties.publish.collections&fields=publishedContent.properties.relatedThreads&fields=publishedContent.properties.seo&fields=publishedContent.properties.threadType&fields=publishedContent.properties.custom',
    # ]

        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)


    def start_requests(self):
        urls = [
            'https://www.nike.com/cn/launch/?s=in-stock',
            'https://api.nike.com/product_feed/threads/v2/?anchor=50&count=50&filter=marketplace(CN)&filter=language(zh-Hans)&filter=inStock(true)&filter=productInfo.merchPrice.discounted(false)&filter=channelId(010794e5-35fe-4e32-aaff-cd2c74f89d61)&filter=exclusiveAccess(true,false)&fields=active&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.nodes&fields=publishedContent.properties.coverCard&fields=publishedContent.properties.productCard&fields=publishedContent.properties.products&fields=publishedContent.properties.publish.collections&fields=publishedContent.properties.relatedThreads&fields=publishedContent.properties.seo&fields=publishedContent.properties.threadType&fields=publishedContent.properties.custom',
        ]
        i = 1;

        for url in urls:
            if i == 1:
                yield scrapy.Request(url=url, callback=self.parse)
            elif i == 2:
                yield scrapy.Request(url=url, callback=self.parse_se)

            i = i + 1


    def parse(self, response):
    	for product_link in response.xpath('//a[@data-qa="product-card-link"]/@href'):
            link_part = product_link.extract()
            link = response.urljoin(link_part)
    		#pname = product.css('.grid-item-info').css('.product-name').css('.product-display-name::text').extract()
    		# print (link)
    		# print (link)
    		#item = NikelItem()
    		#item['product_name'] = product.xpath('//div[@class="grid-item-info"]/div[@class="product-name"]/div[@class="product-display-name"]/p[1]/text()')
    		#item['product_price'] = product.xpath('//div[@class="grid-item-info"]/div[@class="product-name"]/div[@class="product-price"]/div[@class="prices"]/span[2]/text()')
    		#yield item
            yield scrapy.Request(url=link, callback=self.parse_shoe)


    def parse_shoe(self,response):
        name = response.xpath('//title').extract()
        price = response.xpath('//div[@data-qa="price"]/text()').extract()
        item = NikelItem()
        item['product_name'] = name
        item['product_price'] = price
        yield item


    def parse_se(self, response):
        jsd = json.loads(response.body)
        for info in jsd['objects']:
            item = NikelItem()
            name = info['productInfo'][0]['productContent']['fullTitle']
            price = info['productInfo'][0]['merchPrice']['currentPrice']

            item['product_name'] = name
            item['product_price'] = price
            yield item
            
        # print(jsd['objects'][0]['productInfo'][0]['merchPrice']['currentPrice'])
        # print(jsd['objects'][0]['productInfo'][0]['productContent']['fullTitle'])