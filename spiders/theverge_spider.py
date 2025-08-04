import scrapy
from spiders.items import ArticleItem

class TheVergeSpider(scrapy.Spider):
    name = "theverge"
    allowed_domains = ["theverge.com"]
    start_urls = [
        "https://www.theverge.com/space",
        "https://www.theverge.com/search?q=Satellite"
    ]

    def parse(self, response):
        articles = response.css(".c-compact-river__entry")
        for article in articles:
            item = ArticleItem()
            item['title'] = article.css(".c-entry-box--compact__title a::text").get()
            item['url'] = article.css(".c-entry-box--compact__title a::attr(href)").get()
            item['content_text'] = article.css(".c-entry-content ::text").get()
            item['published_date'] = article.css("time::attr(datetime)").get()
            item['author'] = article.css(".c-byline__item a::text").get()
            item['source'] = "The Verge"
            yield item

        next_page = response.css(".c-pagination__next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

