# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Tutorial2Item(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class DmozItem(Item):
	title = Field()
	link = Field()
	desc = Field()

class TestItem(Item):
	id = Field()
	name = Field()
	description = Field()


class CompuindiaItem(Item):
	sourceurl = Field()
	code = Field()
	price = Field()
	color = Field()
	name = Field()
	#
	#~brand
	features = Field()
	specs = Field()
	description = Field()
	moreDescription = Field()
	additionalInfo = Field()
	# Related Products taken itself from the site, not calculated on our end, List of Related Product containing Urls of those products
	relatedProducts = Field()
	
	# Image_urls
	image_urls = Field()
	# Images, as a List of image urls
	# Image_paths instead of Images FTM
	images = Field()
	#~image_paths = Field()
	
	# Rating, pulled from Site
	#~rating
	# Availability, pulled from Site
	#~availability
	
	


class MobilestoreItem(Item):
	sourceurl = Field()
	code = Field()
	price = Field()
	color = Field()
	name = Field()
	
	#
	features = Field()
	specs = Field()
	description = Field()
	moreDescription = Field()
	additionalInfo = Field()
	
	brand = Field()
	category = Field()
	subcategory = Field()
	
	# Image_urls
	big_image_urls = Field()
	image_urls = Field()
	thumbnail_image_urls = Field()
	# Images, as a List of image urls
	# Image_paths instead of Images FTM
	images = Field()
	#~image_paths = Field()
	
	# Rating, pulled from Site
	#~rating
	# Availability, pulled from Site
	#~availability
	
	# Related Products taken itself from the site, not calculated on our end, List of Related Product containing Urls of those products
	relatedProducts = Field()
	


class YepmewomenItem(Item):
	sourceurl = Field()
	code = Field()
	price = Field()
	discountPrice = Field()
	color = Field()
	name = Field()
	sizes = Field()
	
	#
	features = Field()
	specs = Field()
	description = Field()
	moreDescription = Field()
	additionalInfo = Field()
	
	brand = Field()
	category = Field()
	subcategory = Field()
	
	# Image_urls
	big_image_urls = Field()
	image_urls = Field()
	thumbnail_image_urls = Field()
	# Images, as a List of image urls
	# Image_paths instead of Images FTM
	images = Field()
	#~image_paths = Field()
	
	# Rating, pulled from Site
	#~rating
	# Availability, pulled from Site
	#~availability
	
	# Related Products taken itself from the site, not calculated on our end, List of Related Product containing Urls of those products
	relatedProducts = Field()


# =========================

from scrapy.contrib.djangoitem import DjangoItem
from tutsplus.models import Tutsplus
class TutsplusItem(DjangoItem):
	django_model = Tutsplus



