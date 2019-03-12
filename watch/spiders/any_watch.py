import scrapy
from scrapy.http import FormRequest

class Any_watch(scrapy.Spider):
    name = 'Any Watch'
    start_urls = ['https://www.chrono24.com']
    page = 3

    def parse(self, response):
        watch = input('Enter a watch: ')
        return FormRequest.from_response(response, formdata={
            'query': watch,
            'dosearch': 'true',
            'searchexplain': '1',
            'watchTypes': '',
            'accessoryTypes': ''
        }, callback=self.start_parse)

    def start_parse(self, response):
        sum = 0
        count = 0
        price_list = []
        prices = response.css('#wt-watches strong::text').re('\d+\,*\d*\.*\d*')
        for price in prices:
            price = float(price.replace(',', ''))
            price_list.append(price)
        for price in price_list:
            count += 1
            sum += price
        avg = sum / count
        yield {
               'average price': avg,
               'number of watches': count}

        next_page = response.css('.pull-sm-right li:nth-child(' + str(self.page) + ') a::attr(href)').get()
        if self.page < 7 and next_page:
            yield response.follow(next_page, callback=self.start_parse)
            self.page += 1

