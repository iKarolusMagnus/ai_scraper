import scrapy
from spiders.items import ArticleItem

class UktnSpider(scrapy.Spider):
    name = "uktn"
    allowed_domains = ["uktech.news"]
    start_urls = [
        "https://www.uktech.news/space-tech"
    ]

    def parse(self, response):
        articles = response.css(".post-item")
        for article in articles:
            item = ArticleItem()
            item['title'] = article.css(".post-title a::text").get()
            item['url'] = article.css(".post-title a::attr(href)").get()
            item['content_text'] = article.css(".excerpt::text").get()
            item['published_date'] = article.css(".post-date::text").get()
            item['author'] = article.css(".post-author a::text").get()
            item['source'] = "UKTN"
            item['category'] = "Space Tech"
            yield item

        next_page = response.css(".next-page a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
