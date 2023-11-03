# this is to parse through related words.io
# more docstring

import scrapy
from scrapy.linkextractors import LinkExtractor

class wordsSpider(scrapy.Spider):
    name = 'related_words_spider'
    ui="bakery"
    start_urls = ["https://relatedwords.io/"] 

    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.start_urls = [f'https://relatedwords.io/search.pnp?search={self.text}']
  
    def parse(self, response):
        """
        """
        topic_url=response.url + self.ui 
        yield scrapy.Request(topic_url,callback=self.parse_word_links)
     
    def parse_word_links(self, response):
        """
        get the links of first 10 keywords of user input's word
        """
        
        # get first 10 words
        words=response.css('span.term a::text')[0:10].getall()
        
        #gets links from page
        links=self.link_extractor.extract_links(response) 
        
        # get the link for the first 10 related words 
        for link in links[26:35]:
            yield scrapy.Request(link.url, callback = self.parse_related_words)
    
    def parse_related_words(self,response):
        
        words=response.css('span.term a::text')[0:10].getall()
        words.append(response.css('title::text').get().split(" Words")[0].lower())
    
        for word in words:
            yield{
                "topic": self.ui,
                "related_word": word
            }
