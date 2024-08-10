import scrapy
import re
from typing import Any

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://chocolate.co.uk/collections/all"]

    def parse(self, response):
        products = response.css('product-item')
        for product in products:
            print('dasdsads')
            span_price = product.css('span.price').get()
            pattern = r'[£$]\s*(\d+\.\d{2})'
            match: re.Match[str] | Any = re.search(pattern, span_price)
            yield {
                'name': product.css('a.product-item-meta__title::text').get(),
                # 'price': product.css('span.price').get().replace('<span class="price price--highlight"\n'),
                # 'price': product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>',''),
                # 'price': re.sub(r"\£?\d+(\.\d{1,2})?", "", span_price),
                'price': match.group(1),
                'url': product.css('div.product-item-meta a').attrib['href'],
            }
            
        next_page = response.css('[rel="next"] ::attr(href)').get()

        if next_page is not None:
            next_page_url = f'https://www.chocolate.co.uk{next_page}'
            yield response.follow(next_page_url, callback=self.parse)

# https://scrapeops.io/python-scrapy-playbook/scrapy-beginners-guide/#extract-product-details