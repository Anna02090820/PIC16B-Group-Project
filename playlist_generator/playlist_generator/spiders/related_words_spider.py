# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor
import numpy as np

class wordsSpider(scrapy.Spider):
    name = 'related_words_spider'
    ui="bakery"
    start_urls = ["https://relatedwords.io/"] 
    link_extractor = LinkExtractor(allow="https://relatedwords.io/")
  
    def parse(self, response):
        """
        """
        # prob add an if statement to replace spaces with dashes
        # add a raise exception for 404 not found
        word_url=response.url + self.ui 
        yield scrapy.Request(word_url, callback=self.parse_word_links)
     
    def parse_word_links(self, response):
        """
        """
        # create range to iterate through
        num_words= np.zeros(10)
        
        for i in range(num_words):
            # find link to the related word (i + 1) because python is 0-index
            word_link = response.xpath(f"//*[@id=\"terms-list\"]/li[{str(i+1)}]/div[1]/span[1]/a/@href").get()
            
            # create the link for the related words
            next_link = urljoin(response.url, word_link)
            
            yield scrapy.Request(next_link, callback = self.parse_related_words)
    
    def parse_related_words(self, response):
        
        words=response.css('span.term a::text')[0:10].getall()
        
        for word in words:
            yield{
                "topic": self.ui,
                "related_word": word
                }
