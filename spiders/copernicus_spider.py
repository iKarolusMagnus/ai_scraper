import scrapy
from spiders.items import ArticleItem

class CopernicusSpider(scrapy.Spider):
    name = "copernicus"
    allowed_domains = ["dataspace.copernicus.eu"]
    start_urls = [
        "https://dataspace.copernicus.eu/news"
    ]

    def parse(self, response):
        articles = response.css(".news-item")
        for article in articles:
            item = ArticleItem()
            item['title'] = article.css(".news-title a::text").get()
            item['url'] = article.css(".news-title a::attr(href)").get()
            item['content_text'] = article.css(".news-excerpt::text").get()
            item['published_date'] = article.css(".news-date::text").get()
            item['source'] = "Copernicus Data Space Ecosystem"
            item['category'] = "Earth Observation/Satellites"
            yield item

        next_page = response.css(".pagination-next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
