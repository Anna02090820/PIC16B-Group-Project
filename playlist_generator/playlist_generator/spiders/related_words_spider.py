# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor

class playlistSpider(scrapy.Spider):
    name = 'playlist_spider'
    
    start_urls = ["https://relatedwords.io/"] 
  
def parse(self, response):
        """
        """
        ui="bakery"
        cast_url=response.url +ui 
        yield scrapy.Request(cast_url,callback=self.parse_related_words)
        #acesses the cast and crew page

def parse_related_words(self,response):
        
        words=response.css('span.term a::text').get()) #gets number of cast
        
        for link in links[:total_actors]:
            yield scrapy.Request(link.url,callback=self.parse_actor_page) 
            #accesses each actor profile page
