import scrapy
from spiders.items import ArticleItem

class TechCrunchSpider(scrapy.Spider):
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]
    start_urls = [
        "https://techcrunch.com/category/space/",
    ]

    def parse(self, response):
        articles = response.css(".post-block")
        for article in articles:
            item = ArticleItem()
            item['title'] = article.css(".post-block__title__link::text").get()
            item['subtitle'] = article.css(".post-block__header::text").get()
            item['url'] = article.css(".post-block__title__link::attr(href)").get()
            item['content_text'] = article.css(".post-block__content::text").get()
            item['published_date'] = article.css("time::attr(datetime)").get()
            item['author'] = article.css(".river-byline__authors a::text").get()
            item['source'] = "TechCrunch"
            yield item

        next_page = response.css(".load-more a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

