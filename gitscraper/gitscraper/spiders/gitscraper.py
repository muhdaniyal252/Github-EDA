from importlib.util import spec_from_file_location
import scrapy
from ..items import GitscraperItem
import pandas as pd

df = pd.read_csv('/home/daniyal/working/test_marketlytics/Objective_1/responses.csv')

class GitScraperSpider(scrapy.Spider):
    name = 'gitscraper'
    start_urls = list(df['html_url'])
    item = GitscraperItem()

    def parse(self, response, **kwargs):
        stars = int(response.css('span#repo-stars-counter-star').extract()[0].split('title="')[1].split('" ')[0].replace(',',''))
        forks = int(response.css('span#repo-network-counter').extract()[0].split('title="')[1].split('" ')[0].replace(',',''))
        branchs = int(response.css('a.ml-3:nth-child(1) > strong:nth-child(2)::text').extract()[0])
        tags = int(response.css('a.ml-3:nth-child(2) > strong:nth-child(2)::text').extract()[0])
        url = response.url
        
        self.item['stars'] = stars
        self.item['forks'] = forks
        self.item['branchs'] = branchs
        self.item['tags'] = tags
        self.item['url'] = url

        yield self.item
