# MobileStore Spider


import os

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector


import re
import sys

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import *

from tutorial2.items import MobilestoreItem

class MobilestoreSpider(CrawlSpider):
	name = 'mobilestore'
	allowed_domains = ['mobilestore.in', 'themobilestore.in']
	
	# Start Url
	#~start_urls = ['http://www.mobilestore.in/stores']
	# Next Link
	start_urls = ['http://www.themobilestore.in/home-mobiles-&-tablet-mobiles-samsung']
	
	urlList = []
	
	# DONE
	# If you are writing a process_value, then you will  # have to return the links you want. You can not leave it # without returning.
	# process_value
	def pv(value):
		"""This function takes values links from Rules, and can process those links in any manner"""
		# Removing a link having "deals.html" in it, as we dont want that link to be crawled
		
		print "value"
		print value.__dict__
		print dir(value)
		
		#~if re.search('.*deals\.html', value):
			#~return None
		#~else:
			#~return value
		
	
	# NOT USED FTM
	def pl(value):
		#~print sys._getframe().f_code.co_name
		#~print 'value'
		#~print type(value)
		#~print value
		pass
		
	
	# if url like .*/accessories/.* , brand comes from 1st letter of the Name of the product
	# if url like .*mobiles-tablet.* , brand is last node in breadcrumb
	def get_brand(mss, response, hxs):
		if "accessories" in response.url:
			return hxs.select("//div[@id='title']/h1/text()").extract()[0].split(' ')[0]
		elif "mobiles-tablet":
			return hxs.select("//div[@id='browse-nodes']/a/text()")[-1].extract()
		else:
			return None
	
	def parse_item(response):
		#~self.log('Hi, this is an item page! %s' % response.url)
		#~print 'function'
		#~print sys._getframe().f_code.co_name
		#~print 'response'
		#~print response
		#~print type(response)
		#~print "response.url"
		#~print response.url
		
		hxs = HtmlXPathSelector(response)
		# ATM, all these item values are coming in a List type with just the 0th key
		item = MobilestoreItem()
		#
		item['sourceurl'] = [ response.url ]
		#
		# Code: String
		item['code'] = re.search(r'p-(.*)-', response.url ).group(1)
		#
		#~item['price'] = hxs.select("//div[@class='our_price']//span[@class='m-w']/text()").encode('utf-8')
		item['price'] = hxs.select("//div[@class='our_price']//span[@class='m-w']/text()")
		#
		item['color'] = hxs.select("//span[@class='catalog-option-title']/text()")
		#
		item['name'] = hxs.select("//div[@id='title']/h1/text()").extract()[0]
		#
		item['features'] =  [None]
		#
		#~item['specs'] = hxs.select("//div[@id='feature_groups']").extract().encode('utf-8')
		item['specs'] = hxs.select("//div[@id='feature_groups']").extract()
		#
		#~item['description'] = hxs.select("//div[@id='description']/p[@class='MsoNormal']/span/text()").encode('utf-8')
		item['description'] = hxs.select("//div[@id='description']/p[@class='MsoNormal']/span/text()")
		#
		item['moreDescription'] = [None]
		#
		#~item['additionalInfo'] = hxs.select('//div[@id="additional"]').extract()
		item['additionalInfo'] = [None]
		#
		item['relatedProducts'] = [None] # FTM
		
		cat_subcat = hxs.select("//div[@id='browse-nodes']/a")
		# To ADD
		#
		#~item['category'] = hxs.select("//div[@id='browse-nodes']/a")[1]
		item['category'] = cat_subcat[1]
		#
		#~item['subcategory'] = hxs.select("//div[@id='browse-nodes']/a")[2]
		item['subcategory'] = cat_subcat[2]
		
		mss = MobilestoreSpider()
		# if url like .*mobiles-tablet.* , brand is last node in breadcrumb
		# if url like .*/accessories/.* , brand comes from 1st letter of the Name of the product
		item['brand'] = MobilestoreSpider.get_brand(mss, response, hxs)
		
		# To ADD-
		
		#
		# IMAGES
		# Almost, CHECK
		# The whole links are getting selected right now, select just the attribute value
		zoom_imgs = []
		medium_imgs = []
		thumbnail_imgs = []
		zoom_imgs = hxs.select("//ul[@class='thumbnails']/li/a[@data-zoom-url]")
		medium_imgs = hxs.select("//ul[@class='thumbnails']/li/a[@data-medium-url]")
		thumbnail_imgs = hxs.select("//ul[@class='thumbnails']/li/a/img[@src]")
		item['big_image_urls'] = list( set( zoom_imgs ) )
		item['image_urls'] =  list( set(  medium_imgs  ) )
		item['thumbnail_image_urls'] = list( set( thumbnail_imgs ) )
		
		#IMAGES-
		
		#~print 'item'
		#~print item
		#~
		#~sys.exit('S')
		
		return item
		
		
	rules = (
		# Extract links matching 'category.php' (but not matching 'subsection.php')
		# and follow links from them (since no callback means follow=True by default).
		
		### Now 3rd Page
		# Extracting the actual data and images from Product Page
		# FIN THIS
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='col-main']/div[@class='product-view']" ], deny = [".*tata-photon.*",  ] ), callback = parse_item, follow=False ), 
		
		
		### Now 2nd Page
		# ===PAGE 2: DONE===
		# FIN THIS
		#PAGE2: NEXT LINKS
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//a[@class='next_page']", ] ), follow=True ),
		
		# FIN THIS
		# PAGE2: PRODUCT LINKS
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//span[@class='variant-title']" ], ), callback=parse_item, follow=True ),
		
		
		# ===PAGE 1: DONE===
		# Mobilestore.in
		# THIS # FIN THIS
		# DONE
		Rule( SgmlLinkExtractor( restrict_xpaths = [ "//div[@class='header-menu navtree']", ], allow = [ ".*home-mobiles-&-tablet-mobiles-.*", ".*home-mobiles-&-tablet-tablet-.*", ".*home-accessories-.*"], ) , callback=pv, follow=True ),
		
	)
	
	
	
	
