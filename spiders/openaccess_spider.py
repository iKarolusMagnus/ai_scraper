import scrapy
from spiders.items import ArticleItem

class OpenAccessSpider(scrapy.Spider):
    name = "openaccess"
    allowed_domains = ["openaccessgovernment.org"]
    start_urls = [
        "https://www.openaccessgovernment.org/category/open-access-news/"
    ]

    def parse(self, response):
        articles = response.css(".post-item")
        for article in articles:
            title = article.css(".entry-title a::text").get()
            # Filter for space/satellite related articles
            if title and any(keyword in title.lower() for keyword in ['space', 'satellite', 'rocket', 'nasa', 'esa']):
                item = ArticleItem()
                item['title'] = title
                item['url'] = article.css(".entry-title a::attr(href)").get()
                item['content_text'] = article.css(".entry-excerpt p::text").get()
                item['published_date'] = article.css(".entry-date::text").get()
                item['author'] = article.css(".entry-author a::text").get()
                item['source'] = "Open Access Government"
                item['category'] = article.css(".entry-category a::text").get()
                yield item

        next_page = response.css(".next-page a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
