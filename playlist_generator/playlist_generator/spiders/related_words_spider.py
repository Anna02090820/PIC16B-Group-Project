# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor

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
        
        # get first 10 words
        words=response.css('span.term a::text')[0:10].getall()
        
        #gets links from page
        links=self.link_extractor.extract_links(response) 
        
        # get the link for the first 10 related words 
        for link in links[26:35]:
            yield scrapy.Request(link.url, callback = self.parse_related_words)
    
    def parse_related_words(self, response):
        
        words=response.css('span.term a::text')[0:10].getall()
        
        for word in words:
            yield{
                "topic": self.ui,
                "related_word": word
                }
