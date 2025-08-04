import scrapy
from spiders.items import ArticleItem

class WiredSpider(scrapy.Spider):
    name = "wired"
    allowed_domains = ["wired.com"]
    start_urls = [
        "https://www.wired.com/tag/satellites/",
        "https://www.wired.com/tag/space/"
    ]

    def parse(self, response):
        articles = response.css(".SummaryItemWrapper-iwvBff")
        for article in articles:
            item = ArticleItem()
            item['title'] = article.css(".SummaryItemHedBase-hiFYpQ::text").get()
            item['url'] = article.css(".SummaryItemHedLink-civMjp::attr(href)").get()
            item['content_text'] = article.css(".SummaryItemContent-eiDYMl ::text").get()
            item['published_date'] = article.css("time::attr(datetime)").get()
            item['author'] = article.css(".SummaryItemByline-dSYKKG a::text").get()
            item['source'] = "Wired"
            yield item

        next_page = response.css(".next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
