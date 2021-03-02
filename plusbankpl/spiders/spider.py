import scrapy

from scrapy.loader import ItemLoader
from ..items import PlusbankplItem
from itemloaders.processors import TakeFirst


class PlusbankplSpider(scrapy.Spider):
	name = 'plusbankpl'
	start_urls = ['https://plusbank.pl/o-banku/biuro-prasowe/aktualnosci']

	def parse(self, response):
		post_links = response.xpath('//div[@class="content"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="tekst news"]/div[@class="title"]/text()').get()
		description = response.xpath('//div[@class="tekst news"]//text()[normalize-space() and not(ancestor::button | ancestor::div[@class="title"] | ancestor::div[@class="date"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="tekst news"]/div[@class="date"]/text()').get()

		item = ItemLoader(item=PlusbankplItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
