# Homeshop18 Spider
# Run Command
# scrapy crawl homeshop18 -o downloaded_items/homeshop18/homeshop18.json -t json

import os

from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import *

from tutorial2.items import *

import re
import sys

class Homeshop18Spider(CrawlSpider):
	counter = 0

	# name of the spider to run from terminal
	name = 'homeshop18'
	allowed_domains = ['homeshop18.com']
	
	start_urls = [
		"http://www.homeshop18.com/mobiles/category:3024/?it_category=MN&it_action=MA-AAMNTL&it_label=MN-AAMNTL-130822115933-PD-MA-RM-OT-CA_Mobiles&it_value=0",
		"http://www.homeshop18.com/computers-26-tablets/category:3254/?it_category=MN&it_action=CT-ADMNTL&it_label=MN-ADMNTL-130822115933-PD-CT-RM-OT-CA_ComputersAndTablets&it_value=0",
		"http://www.homeshop18.com/electronics/category:3203/?it_category=MN&it_action=EL-ACMNTL&it_label=MN-ACMNTL-130822115933-PD-EL-RM-OT-CA_ElectronicsAndCarCare&it_value=0",
		"http://www.homeshop18.com/cameras-26-accessories/category:3159/?it_category=MN&it_action=CC-ABMNTL&it_label=MN-ABMNTL-130822115933-PD-CC-RM-OT-CA_CamerasAndAccessories&it_value=0",
		"http://www.homeshop18.com/travel-26-luggage/category:17331/",


		# "http://www.homeshop18.com/men/category:14967/inStock:true/?it_category=MN&it_action=CL-BAMNTL&it_label=MN-BAMNTL-140603181150-PR-CL-RM-OT-SC_MEN&it_value=0",
		# "http://www.homeshop18.com/men/category:15053/inStock:true/?it_category=MN&it_action=FW-HAMNTL&it_label=MN-HAMNTL-130913140858-PR-FW-RM-OT-SC_MensFootwear&it_value=0",
		# "http://www.homeshop18.com/men/category:15097/inStock:true/?it_category=MN&it_action=FA-GBMNTL&it_label=MN-GBMNTL-140617112816-PR-FA-AR-OT-SC_Men-0_0-0-MN02TL-FA-140617-AR-OT-SR&it_value=0",
		# "http://www.homeshop18.com/micromax-canvas-juice-a177-dual-sim-android-mobile-phone-black/mobiles/mobile-phones/product:31800171/cid:3027/?it_category=CP&it_action=MA-GRI001&it_label=CP-GRI001-141120170809-31800171-PD-MA-OP-OT-GT_SmartphonesAndAccessories-0_SmartphonesAndAccessories-0-GDThem-MA-140909-OP-OT-GT&it_value=0",

	]
	
	# DONE
	# If you are writing a process_value, then you will 
	# have to return the links you want. You can not leave it
	# without returning.
	# process_value
	# NOT USED FTM
	def pv(value):
		"""This function takes values links from Rules, and can process those links in any manner"""
		
		Homeshop18Spider.counter += 1
		c = Homeshop18Spider.counter
		# if Homeshop18Spider.counter == 1:
		# 	return value
		print c
		print value
		return None
	
	def parse_item(response):
		# Homeshop18Spider.counter += 1
		# c = Homeshop18Spider.counter
		# print c
		# print response.url
		# item = None

		hxs = HtmlXPathSelector(response)
		h = hxs
		item = Homeshop18Item()
		item['sourceurl'] = [ response.url ]
		item['code'] = h.select("//span[@id='productCodeInPDP']/text()").extract()[0] if h.select("//span[@id='productCodeInPDP']/text()").extract() else None # Code: String 
		item['discounted_selling_price'] = h.select("//span[@id='hs18Price']/text()").extract()[1].strip() if h.select("//span[@id='hs18Price']/text()").extract() else None
		item['color'] = Homeshop18Spider.get_color(hxs)
		item['name'] = ' ' . join( h.select("//td[@class='specs_key']/span[contains(text(), 'Model')]/../following-sibling::td/span/text()").extract() )
		item['features'] = h.select("//ul[@class='keyfeature_neo']").extract()
		item['specs'] = h.select("//div[@id='productSpecificationDetailsAreaPDP']").extract()
		item['description'] = Homeshop18Spider.get_description(hxs)
		item['weight'] = Homeshop18Spider.get_weight(hxs)
		item['dimension'] = Homeshop18Spider.get_dimension(hxs)
		item['delivery_time'] = h.select("//span[@id='deliverySLA']/text()").extract()[0] if h.select("//span[@id='deliverySLA']/text()").extract() else None
		item['price'] = h.select("//em[@id='mrpPrice']/text()").extract()[0].strip() if h.select("//em[@id='mrpPrice']/text()").extract() else None
		item['discount_percent'] = h.select("//span[@id='discount']/text()").extract()[0] + '%' if h.select("//span[@id='discount']/text()").extract() else None
		all_cats = h.select("//td[@id='productCategoryInHighLightsPDP']/text()").extract()[0] if h.select("//td[@id='productCategoryInHighLightsPDP']/text()").extract() else None
		item['product_type'] = all_cats
		item['category'] = all_cats
		item['subcategory'] = [None]
		item['brand'] = h.select("//a[@id='productBrandInHighlightsPDP']/@title").extract()[0] if h.select("//a[@id='productBrandInHighlightsPDP']/@title").extract() else None
		item['reviews'] = h.select("//div[@class='pdp_details_review_count']/@content").extract()[0] if h.select("//div[@class='pdp_details_review_count']/@content").extract() else None
		item['ratings'] = h.select("//div[@class='rating']/span/text()").extract()[0] if h.select("//div[@class='rating']/span/text()").extract() else None
		#IMAGES
		item['image_urls'] = Homeshop18Spider.get_imgs(hxs)
		#IMAGES-
		
		# item['material_fabric'] = 
		# item['payment_options'] = hxs.select("//span[@class='emi-text']/text()").extract()[0]
		# item['seller_info'] = hxs.select("//a[@class='seller-name']/text()").extract()[0]

		return item


	@staticmethod
	def get_color(h):
		col = h.select("//span[@id='productTitleInPDP']/text()").extract()
		if col:
			col = col[0]
			if col.find('-') != -1:
				col = col.split('-')
				if col:
					col = col[1].strip()

		return col


	@staticmethod
	def get_description(h):
		desc = None
		desc = h.select("//span[@id='productDescriptionTextPDP']/text()").extract()
		if desc:
			desc = desc[0].encode('utf-8')
		return desc


	@staticmethod
	def get_imgs(hxs):
		imgs = None
		imgs = hxs.select("//ul[@class='photo-slider clearfix']//a/img/@src").extract()
		li = []
		for i in imgs:
			st = i.replace('-small_', '-large_')
			st = 'http:'+st
			li.append(st) 
		return li

	@staticmethod
	def get_weight(h):
		weight = None
		weight = h.select("//span[contains(text(), 'Weight')]/../following-sibling::td[@class='specs_value']/span/text()").extract()
		if weight:
			return weight[0]
		return weight

	@staticmethod
	def get_dimension(h):
		ret = None
		ret = h.select("//span[contains(text(), 'Dimension')]/../following-sibling::td[@class='specs_value']/span/text()").extract()
		if ret:
			return ret[0]
		return ret


	rules = (
		# content grid-view clearfix
		# Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[contains(@class, 'box')]/div[@class='inside']" ], process_value=pv ), ),

		# Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='inside']" ], unique=True , process_value=pv ), ),
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='inside']" ], ), callback = parse_item ),
	)
	
	



