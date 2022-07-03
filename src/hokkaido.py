import scrapy


class HokkaidoSpider(scrapy.Spider):
    name = 'hokkaido'
    allowed_domains = ['kensa-hokkaido.jp']
    start_urls = ['https://kensa-hokkaido.jp/list/']

    def parse(self, response):
        city_links = response.css('.area_list > a')
        for city_link in city_links:
            city_page_url = response.urljoin(city_link.attrib['href'])
            yield scrapy.Request(city_page_url, callback=self.parse_city)

    def parse_city(self, response):
        city_name = response.css('.search_city_head > h3::text').get()
        places = response.css('.search_city_list > .office')
        for place in places:
            name = place.css('.office_head > h4::text').get()
            address_part = place.css('.office_head > address::text').get()
            types = [dt.get() for dt in place.css('.office_body > .type dt ::text')]
            pcr_test = 'PCR' in types
            antigen_test = '抗原定性検査' in types
            address = f'北海道 {address_part}'
            yield {'name': name, 'address': address, 'pcr_test': pcr_test, 'antigen_test': antigen_test}
