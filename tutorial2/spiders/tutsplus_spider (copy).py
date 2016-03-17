# Tutsplus Spider

import os
import re
import sys
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tutorial2.items import TutsplusItem
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy.item import *


class TutsplusSpider(BaseSpider):
	name = 'tutsplus'
	allowed_domains = ['tutsplus.com']
	start_urls = ['http://webdesign.tutsplus.com/courses/become-a-css-superhero-with-stylus']
	
	
	# def parse(self, response):

	# 	# t = TutsplusItem()
	# 	# print "t"
	# 	# print t
	# 	# print dir(t)

	# 	hxs = HtmlXPathSelector(response)

	# 	l = XPathItemLoader(item=TutsplusItem(), response=response)

	# 	url = response.url
	# 	l.add_value('tutUrl', url)
	# 	l.add_xpath('tutTitle', '//h1[@class="content-header__title"]/text()')

	# 	for i in hxs.select('//div[@class="course-meta__item"]'):
	# 		string = i.select('div[@class="course-meta__label"]/text()').extract()[0]

	# 		if "Less" in string:
	# 			lessons = i.select('div[@class="course-meta__value"]/text()').extract()

	# 		if "Leng" in string:
	# 			length = float( i.select('div[@class="course-meta__value"]/text()').extract()[0].split(' ')[0] )

	# 		if "Categ" in string:
	# 			span = i.select('//span[@class="course-meta__tag"]')
	# 			for k in span:
	# 				texts = k.select("a/text()").extract()
	# 				links = k.select("a/@href").extract()

	# 			cats = str( dict (zip(texts, links)) )

	# 	l.add_value('tutLength', length)
	# 	l.add_xpath('authorName', '//a[@class="content-header__author-link"]/text()')
	# 	l.add_xpath('authorBio', '//div[@class="instructor-bio__details"]/text()')
	# 	l.add_xpath('authorAboutLink', '//a[@class="content-header__author-link"]/@href')
	# 	l.add_value('numberOfLessons', lessons)
	# 	l.add_value('categories', cats)
	# 	l.add_xpath('courseDescription', '//div[@class="course__description"]/p/text()')

	# 	fees = hxs.select('//a[@class="buy-course-button__purchase-link"]/text()').extract()[0]
	# 	fee = re.search("\$(\d+)", fees)
	# 	fee = fee.group(1)
	# 	l.add_xpath('courseFees', fee)
	# 	l.add_xpath('courseFeeLink', '//a[@class="buy-course-button__purchase-link"]/@href')
	# 	l.add_xpath('courseStartDate', '//time[@class="content-header__publication-date"]/@datetime')


	# 	# i.save()
	# 	# tuts = TutsplusItem(l)
	# 	# print tuts
	# 	# print l.load_item()

	# 	i = l.item
	# 	print "i"
	# 	print i
	# 	print dir(i)
	# 	# i.save()

	# 	print "l"
	# 	print dir(l)

	# 	return l.load_item()


	def parse(self, response):

		hxs = HtmlXPathSelector(response)

		l = TutsplusItem()

		url = response.url
		l['tutUrl'] = url
		l['tutTitle'] = hxs.select('//h1[@class="content-header__title"]/text()').extract()[0]

		for i in hxs.select('//div[@class="course-meta__item"]'):
			string = i.select('div[@class="course-meta__label"]/text()').extract()[0]

			if "Less" in string:
				lessons = i.select('div[@class="course-meta__value"]/text()').extract()

			if "Leng" in string:
				length = float( i.select('div[@class="course-meta__value"]/text()').extract()[0].split(' ')[0] )

			if "Categ" in string:
				span = i.select('//span[@class="course-meta__tag"]')
				texts = span.select("a/text()").extract()
				links = span.select("a/@href").extract()

				cats = str( dict (zip(texts, links)) )

		l['tutLength'] = length
		l['authorName'] = hxs.select('//a[@class="content-header__author-link"]/text()').extract()[0]
		l['authorBio'] = hxs.select('//div[@class="instructor-bio__details"]/text()').extract()[0]
		l['authorAboutLink'] = hxs.select('//a[@class="content-header__author-link"]/@href').extract()[0]
		l['numberOfLessons'] = lessons[0]
		l['categories'] = cats
		l['courseDescription'] = hxs.select('//div[@class="course__description"]/p/text()').extract()[0]
		fees = hxs.select('//a[@class="buy-course-button__purchase-link"]/text()').extract()[0]
		fee = re.search("\$(\d+)", fees)
		fee = fee.group(1)
		l['courseFees'] = fee
		l['courseFeeLink'] = hxs.select('//a[@class="buy-course-button__purchase-link"]/@href').extract()[0]
		l['courseStartDate'] = hxs.select('//time[@class="content-header__publication-date"]/@datetime').extract()[0]


		# i.save()
		# tuts = TutsplusItem(l)
		# print tuts
		# print l.load_item()

		# i = l.item
		i = l
		l.save()

		print "i"
		print i
		print dir(i)
		# i.save()

		print "l"
		print dir(l)

		return l
