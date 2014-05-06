# http://www.pricedealsindia.com Spider
# Pricedealsindia

# 

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import *

from tutorial2.items import CompuindiaItem

import sys
import re
import os

class PricedealsindiaSpider(CrawlSpider):
	name = 'pricedealsindia'
	allowed_domains = ['pricedealsindia.com']
	start_urls = ['http://www.pricedealsindia.com']
	
	urlList = []
	
	# DONE
	# If you are writing a process_value, then you will 
	# have to return the links you want. You can not leave it
	# without returning.
	# process_value
	# NOT USED FTM
	def pv(value):
		"""This function takes values links from Rules, and can process those links in any manner"""
		# Removing a link having "deals.html" in it, as we dont want that link to be crawled
		if re.search('.*deals\.html', value):
			return None
		else:
			return value
	
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
		#~print 'response'
		#~print response
		#~print type(response)
		#~print "response.url"
		#~print response.url
		
		hxs = HtmlXPathSelector(response)
		
		# ATM, all these item values are coming in a List type with just the 0th key
		item = CompuindiaItem()
		
		item['sourceurl'] = [ response.url ]
		
		#~item['code'] = hxs.select('//td[@class="data"]/text()')[0].extract() # Code: Unicode
		item['code'] = hxs.select('//td[@class="data"]/text()')[0].extract().encode('utf-8') # Code: String
		
		item['price'] = hxs.select('//span[@class="price"]/text()')[0].extract().encode('utf-8')
		
		# left
		item['color'] = [None]
		# Try to do matching with class="last odd"
		#~item['color'] = hxs.select('//tbody/tr[@class="last odd"]') 
		
		item['name'] = hxs.select("//div[@class='product-name']/h1/text()").extract()[0]
		
		#~item['features'] =  hxs.select('//ul[@class="config_listing_pd_page"]/li').extract()
		item['features'] =  hxs.select('//ul[@class="config_listing_pd_page"]/li/text()').extract()
		
		#~item['specs'] = hxs.select('//div[@class="box-collateral box-additional"]').extract()
		item['specs'] = hxs.select('//div[@class="box-collateral box-additional"]').extract()[0].encode('utf-8')
		
		#~item['description'] = hxs.select('//div[@class="box-collateral box-description"]').extract()
		item['description'] = hxs.select('//div[@class="box-collateral box-description"]').extract()[0].encode('utf-8')
		
		item['moreDescription'] = [None]
		
		#~item['additionalInfo'] = hxs.select('//div[@id="additional"]').extract()
		item['additionalInfo'] = hxs.select('//div[@id="additional"]').extract()[0].encode('utf-8')
		
		item['relatedProducts'] = [None] # FTM
		
		#IMAGES
		main_img = []
		image_urls = []
		main_img = hxs.select("//p[@class='product-image']/a/@href").extract()
		img_urls = hxs.select("//div[@class='more-views']/ul/li/a/@href").extract()
		
		item['image_urls'] =  list( set( main_img + img_urls ) )
		#IMAGES-
		
		#~print 'item'
		#~print item
		#~
		#~sys.exit('S')
		
		return item
		
		
	rules = (
		# Pricedealsindia.com
		
		#PAGE2: NEXT LINKS
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//a[@class='next i-next']", ] ), follow=True ),
		
		# PAGE2: PRODUCT LINKS
		###
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='listBlocks productBlocks']" ], deny = [".*dir=.*", ],  ), callback=parse_item , follow = False ),
		
		
		# PAGE 1: 
		# Awesome!!!
		Rule( SgmlLinkExtractor( restrict_xpaths = "//li[@class='level1-li sub']/a", deny = ["/coupons/"], ) , follow=False ),
	)
	
	
	
