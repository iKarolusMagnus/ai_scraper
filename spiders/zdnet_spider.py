import scrapy
from spiders.items import ArticleItem

class ZdnetSpider(scrapy.Spider):
    name = "zdnet"
    allowed_domains = ["zdnet.com"]
    start_urls = [
        "https://www.zdnet.com/topic/space/"
    ]

    def parse(self, response):
        articles = response.css(".c-shortcodeListicle__item")
        for article in articles:
            item = ArticleItem()
            item['title'] = article.css(".c-shortcodeListicle__title a::text").get()
            item['url'] = article.css(".c-shortcodeListicle__title a::attr(href)").get()
            item['content_text'] = article.css(".c-shortcodeListicle__summary::text").get()
            item['published_date'] = article.css("time::attr(datetime)").get()
            item['author'] = article.css(".c-shortcodeListicle__author a::text").get()
            item['source'] = "ZDNet"
            item['category'] = "Space"
            yield item

        next_page = response.css(".c-pagination__next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
