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
		l.save()

		return l
