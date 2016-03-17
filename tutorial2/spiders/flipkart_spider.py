# CompuIndia Spider

# Needed 
# 21 + 25 + 65 + 13 + 41 = 165 in CompuIndia
#1] Got: only, 106, total products/items are around 165 on website, CHECK Y? - 
#2] GET IMAGES NOW - DONE
#3] In IMAGES, item['image_paths'] have not come in json file, check y?, item['image_paths'] is mentioned in ImagePipelines - 


import os

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from tutorial2.items import CompuindiaItem

import re

"""
filename = response.url.split("/")[-2]
self_name = self.__class__.__name__
f = 'responses/' + self_name 
if not os.path.exists(f):
	os.makedirs(f)
f = f + '/' + filename
open(f, 'w+').write(response.body)
#~
"""

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import *

from tutorial2.items import *

import sys

class FlipkartSpider(CrawlSpider):
	counter = 0

	name = 'flipkart'
	allowed_domains = ['flipkart.com']
	
	start_urls = [
		# "http://www.flipkart.com/mobiles/~new-releases/pr?sid=tyy%2C4io",
		# "http://www.flipkart.com/laptops/~hottest/pr?sid=6bo,b5g",
		# "http://www.flipkart.com/home-entertainment/televisions/~popular-televisions/pr?sid=ckf,czl",
		# "http://www.flipkart.com/computers/storage/pen-drives/pr?sid=6bo,jdy,uar",
		# "http://www.flipkart.com/computers/audio-players/home-audio/speakers/pr?sid=6bo,ord,rlj,8sb",
		# "http://www.flipkart.com/beauty-and-personal-care/fragrances/perfumes/pr?p%5B%5D=sort%3Dpopularity&sid=t06%2Cr3o%2Caa1",

		# "http://www.flipkart.com/xolo-a500s-lite/p/itmdwhg8jvsvnvhz?pid=MOBDXSGPRQT6ZWEM&ref=f3ac8dd2-a4d0-4eca-8baa-28da6a2a1ae4&srno=b_9",
		# "http://www.flipkart.com/lenovo-vibe-x2-4g/p/itmef966ajbgseja?pid=MOBEF9643YBYZMF7&srno=b_1&ref=cc7a7fe7-91fc-4787-8615-1a649c442b27",
		"http://www.flipkart.com/lenovo-vibe-x2-4g/p/itmef966ajbgseja",
	]
	
	urlList = []
	prodSpecs = None

	# DONE
	# If you are writing a process_value, then you will 
	# have to return the links you want. You can not leave it
	# without returning.
	# process_value
	# NOT USED FTM
	def pv(value):
		"""This function takes values links from Rules, and can process those links in any manner"""
		FlipkartSpider.counter += 1
		c = FlipkartSpider.counter
		return None
		# else:
		# 	return value
	
	# NOT USED FTM
	def pl(value):
		print sys._getframe().f_code.co_name
		print 'value'
		print type(value)
		print value
		print 'length: ' + str( len(value))
		sys.exit('X')
	
	def parse_item(response):
		#~self.log('Hi, this is an item page! %s' % response.url)
		#~print 'function'
		#~print sys._getframe().f_code.co_name

		hxs = HtmlXPathSelector(response)
		item = FlipkartItem()
		prodSpecs = hxs.select("//div[@class='productSpecs specSection']")
		FlipkartSpider.prodSpecs = prodSpecs
		item['sourceurl'] = [ response.url ]
		# item['code'] = prodSpecs.select("//td[contains(text(), 'Model ID')]/following-sibling::td/text()").extract()[0].encode('utf-8') # Code: String
		item['code'] = [None]

		item['price'] = FlipkartSpider.get_price(hxs)
		item['color'] = FlipkartSpider.get_color(hxs)
		item['name'] = FlipkartSpider.get_name(hxs)
		item['features'] =  hxs.select("//div[@class='keyFeatures specSection']").extract()
		item['specs'] = prodSpecs.extract()[0].strip().encode('utf-8')
		item['description'] = hxs.select("//div[@class='rpdSection']//p[@class='description']/text()").extract()[0].encode('utf-8')
		item['weight'] = hxs.select("//th[contains(text(), 'Dimension')]/../..//td[contains(text(), 'Weight')]/following-sibling::td/text()").extract()
		item['dimension'] = hxs.select("//th[contains(text(), 'Dimension')]/../..//td[contains(text(), 'Size')]/following-sibling::td/text()").extract()
		# Delivery: 1 Day
		item['delivery_time'] = 1
		item['discounted_selling_price'] = FlipkartSpider.get_disc_price(hxs)
		item['discount_percent'] = hxs.select("//span[@class='discount fk-green']/text()").extract()[0].split(' ')[0] or None
		all_cats = hxs.select("//li[@class='fk-inline-block']/a/text()").extract()
		item['product_type'] = all_cats[1]
		# item['material_fabric'] = 
		item['category'] = all_cats[1]
		item['subcategory'] = all_cats[2]
		item['brand'] = prodSpecs.select("//td[contains(text(), 'Brand')]/following-sibling::td/text()").extract()[0]
		item['payment_options'] = hxs.select("//span[@class='emi-text']/text()").extract()[0]
		item['seller_info'] = hxs.select("//a[@class='seller-name']/text()").extract()[0]
		item['reviews'] = hxs.select('//a[@class="review"]/span/text()').extract()
		item['ratings'] = hxs.select("//div[@class='bigStar']/text()").extract()[0]
		#IMAGES
		item['image_urls'] = hxs.select("//div[@class='imgWrapper']/img/@data-src").extract()
		#IMAGES-
		
		return item

	@staticmethod
	def get_name(hxs):
		name = None
		name = hxs.select("//td[contains(text(), 'Name')]/following-sibling::td/text()").extract()
		if name:
			name = name[0].strip()

		if not name:
			name = hxs.select("//h1[@class='title']/text()").extract()
			if name:
				name = name[0].split(' ')[1]

		return name

	@staticmethod
	def get_price(hxs):
		price = None
		price = hxs.select("//span[@class='price list']/text()").extract()
		if price:
			price = price[0].strip().strip('Rs. ')
		if not price:
			price = hxs.select("//span[@class='selling-price omniture-field']/text()").extract()
			if price:
				price = price[0].strip().strip('Rs.').encode('utf-8')

		if not price:
			price = hxs.select("//span[@id='exchangePrice']/text()").extract()
			if price:
				price = price[0]

		return price

	@staticmethod
	def get_disc_price(hxs):
		disc_price = hxs.select("//span[@class='selling-price omniture-field']/text()").extract()[0].strip().strip('Rs.').encode('utf-8')
		if not disc_price:
			disc_price = None
		return disc_price
	
	@staticmethod
	def get_color(hxs):
		prodSpecs = FlipkartSpider.prodSpecs
		color = None
		color = prodSpecs.select("//th[contains(text(), 'GENERAL')]/../..//td[contains(text(), 'Color')]/following-sibling::td/text()").extract()
		if color:
			color = color[0]
		return color


	rules = (
		Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@id='products']//a[@class='fk-display-block']", ), callback = pv, follow=True),
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@id='fk-mainbody-id']" ], ), callback=parse_item , follow = False ),
	)
	
	



