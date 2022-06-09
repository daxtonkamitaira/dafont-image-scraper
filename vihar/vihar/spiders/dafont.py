import scrapy
import string
from vihar.items import ImgItem


class DafontSpider(scrapy.Spider):
    name = 'dafont'
    allowed_domains = ['dafont.com']
    start_urls = []
    lettre = string.ascii_lowercase
    base_url = 'https://www.dafont.com/alpha.php'

    def __init__(self):
        for ch in self.lettre:
            self.start_urls.append(f'{self.base_url}?lettre={ch}')

    def img_parse(self, response):
        item = ImgItem()

        img_url = response.xpath('//div[@style="float:left;width:830px;border-top:1px solid white"]/img/@src').get()

        item['image_urls'] = [response.urljoin(img_url)]
        
        yield item

    def font_parse(self, response):
        font_urls = response.xpath('//div[@class="preview"]/a/@href')

        for font_url in font_urls:
            yield response.follow(url=font_url.get(), callback=self.img_parse)

    def parse(self, response):
        page_count = int(response.xpath('//div[@class="noindex"]')[0].xpath('./a/text()')[-1].get())
        
        for page_number in range(1, page_count+1):
            page_url = f'{response.url}&page={page_number}'
            
            yield scrapy.Request(url=page_url, callback=self.font_parse)
