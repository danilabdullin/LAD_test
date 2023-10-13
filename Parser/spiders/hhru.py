import scrapy
from jobparser.items import JobparserItem
from scrapy.http import HtmlResponse


class HhruSpider(scrapy.Spider):
    name = "hhru"
    allowed_domains = ["hh.ru"]
    start_urls = ["https://hh.ru/search/vacancy?text=Data+Science&area=1&hhtmFrom=main"]

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='serp-item__title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").extract_first()
        salary = response.xpath("//span[@data-qa='vacancy-salary-compensation-type-gross']/text()").extract()
        experience = response.xpath("//span[@data-qa='vacancy-experience']/text()").extract_first()
        yield JobparserItem(name=name, salary=salary, experience=experience)
