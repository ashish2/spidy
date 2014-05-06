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
import sys

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

import sys

class CompuindiaSpider(CrawlSpider):
	name = 'compuindia'
	allowed_domains = ['compuindia.com']
	start_urls = ['http://www.compuindia.com']
	#~start_urls = ['http://www.compuindia.com/touch-pc.html']
	#~start_urls = ['http://www.compuindia.com/touch-pc/new-inspiron-242.html']
	
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
		# Extract links matching 'category.php' (but not matching 'subsection.php')
		# and follow links from them (since no callback means follow=True by default).
		
		### Now 3rd Page
		# Extracting the actual data and images from Product Page
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='product-name']" ] ), callback=parse_item, follow=False ), 
		
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='product-view']" ], deny = [".*tata-photon.*",  ] ), callback=parse_item, follow=True ), 
		# FIN THIS
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='product-view']" ], deny = [".*tata-photon.*",  ] ), callback = parse_item, follow=False ), 
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='col-main']/div[@class='product-view']" ], deny = [".*tata-photon.*",  ] ), callback = parse_item, follow=False ), 
		
		
		### Now 2nd Page
		#~Rule( SgmlLinkExtractor( restrict_xpaths = "//h4[@class='product-name']", process_value= pv2 ), follow=False ),
		#~Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@class='category-products']", process_value= pvN ), follow=False ),
		#~Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@class='category-products']", process_value= pvN ), follow=False ),
		#~Rule( SgmlLinkExtractor( restrict_xpaths="//h4[@class='product-name']", process_value= pvn ), follow=True ),
		# This time i dont need to do process_links
		#~Rule( SgmlLinkExtractor( restrict_xpaths="//h4[@class='product-name']" ), process_links=pl, follow=True ),
		
		# ===PAGE 2: DONE===
		# THESE 2, put it as, list in "restrict_xpaths"
		# IF:
		# THIS
		#~Rule( SgmlLinkExtractor( restrict_xpaths="//h4[@class='product-name']" ), follow=True ),
		# THIS
		#~Rule( SgmlLinkExtractor( restrict_xpaths="//a[@class='next i-next']" ), process_links=pl, follow=True ),
		# ELSE:
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//h4[@class='product-name']", "//a[@class='next i-next']", ] ), process_links=pl, follow=True ),
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//h4[@class='product-name']", "//a[@class='next i-next']", ] ), process_links=pl, follow=False ),
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//h4[@class='product-name']", "//a[@class='next i-next']", ] ), follow=True ),
		
		# FIN THIS
		#PAGE2: NEXT LINKS
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//a[@class='next i-next']", ] ), follow=True ),
		
		# FIN THIS
		# PAGE2: PRODUCT LINKS
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//h4[@class='product-name']" ] ), follow = True ),
		Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='category-products']" ], deny = [".*dir=.*", ".*order=.*", ],  ), callback=parse_item , follow = False ),
		#~Rule( SgmlLinkExtractor( restrict_xpaths=[ "//div[@class='category-products']/ul[@class='products-grid']" ] ), follow = True ),
		
		# Not working
		#~Rule( SgmlLinkExtractor( restrict_xpaths="//a[starts-with(., 'next')]" ), process_links=pl, follow=True ),
		
		# ===PAGE 1: DONE===
		# CompuIndia.com
		### 1st Page
		# Awesome!!!
		# Now links are getting extracted from first page,
		# now go to next page, add another rule & get the item links, with another rule,
		# then third page which is actual product page, extract real data from there
		#~Rule( SgmlLinkExtractor( deny = ( 'deals\.html', ), restrict_xpaths = "//div[@class='parentMenu']", process_value= pv ), follow=True ),
		
		#~Rule( SgmlLinkExtractor( deny= re.compile('.*deals\.html', re.I), restrict_xpaths = "//div[@class='parentMenu']", process_value= pv ), follow=True ),
		# Since i m putting process_value, i have to do a return value and return None, wherever necessary, otherwise the parser stops following links
		# as they haven't been returned
		# THIS
		#~Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@class='parentMenu']", process_value= pv ) , follow=True ),
		# FIN THIS
		Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@class='parentMenu']", deny = [".*deals\.htm.*"], ) , follow=True ),
		#~Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@class='parentMenu']", deny = [".*deals\.htm.*"], process_value= pv ) , follow=True ),
		
		#~Rule( SgmlLinkExtractor(process_value=pv) , follow=False  ),
		
		#~Rule( SgmlLinkExtractor( deny = 'deals\.html', restrict_xpaths = "//div[@class='menu']", process_value= pv ), follow=True ),
		#~Rule( SgmlLinkExtractor( deny = 'deals\.html', restrict_xpaths = "//div[@id='custommenu']", process_value= pv ), follow=True ),
		
		
		# Y is this following?
		#~Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@id='custommenu']", process_value= pv ), follow=False ),
		# Working too.
		#~Rule( SgmlLinkExtractor( process_value= pv ), follow=False ),
		
		#~Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@class='parentMenu']" ) , callback = "chk_urls" ),
		#~Rule( SgmlLinkExtractor( restrict_xpaths = "//div[@class='custommenu']" ) , process_links = "chk_urls" ),
		
		#~Rule( SgmlLinkExtractor( restrict_xpaths = ["//div[@class='parentMenu']/a/@href", ] ) , follow=True, process_request = "chk_urls" ),
		
		#~Rule( SgmlLinkExtractor( ) , process_request = "chk_urls" ),
		
		# Extract links matching 'item.php' and parse them with the spider's method parse_item
		#~Rule( SgmlLinkExtractor( allow=('item\.php', ) ), callback='parse_item' ),
	)
	
	
	
	
	#~def parse_start_url(self, response):
		#~print "parse_start_url"
		#~print 'response'
		#~print response
		#~
		#~pass
		
	
	#~def parse_item(self, response):
		#~print "response"
		#~print response
		#~
		#~item = CompuindiaItem()
		#~item['url'] = response.url
		#~
		#~return item
		#~print "self.urlList"
		#~print self.urlList
		#~pass
		#~
		#~return 
		
