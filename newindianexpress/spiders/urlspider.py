import scrapy
import re
import codecs
import json

class QuotesSpider(scrapy.Spider):
    name = "urlspider"

    def start_requests(self):
        urls = [
            'http://www.newindianexpress.com/topic?term=&request=MIN&type=&row_type=A&archive=true&year=2009',
            'http://www.newindianexpress.com/topic?term=&request=MIN&type=&row_type=A&archive=true&year=2010',
            'http://www.newindianexpress.com/topic?term=&request=MIN&type=&row_type=A&archive=true&year=2011',
            'http://www.newindianexpress.com/topic?term=&request=MIN&type=&row_type=A&archive=true&year=2012',
            'http://www.newindianexpress.com/topic?term=&request=MIN&type=&row_type=A&archive=true&year=2013',
            'http://www.newindianexpress.com/topic?term=&request=MIN&type=&row_type=A&archive=true&year=2014',
            'http://www.newindianexpress.com/topic?term=&request=MIN&type=&row_type=A&archive=true&year=2015',
            'http://www.newindianexpress.com/topic?term=&request=MIN&type=&row_type=A&archive=true&year=2016',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
#        urls = response.xpath('//table[@class="cnt"][last()]//tr[last()]/td[@width="670"]/div[last()]//a/@href').extract()
        print(response.url)
        urlfilename = re.sub(r"\/|:", r"_", response.url)
        with open("./urlhtmls/%s" %urlfilename, 'wb') as g:
            g.write(response.body)
        urls = response.xpath('//div[@class="search-row_type"]//a/@href').extract()
        filename = 'urls.jl'
        with codecs.open(filename, 'a', 'utf-8') as f:
            for rl in urls:
                line = json.dumps(rl,ensure_ascii=False) + "\n"
                f.write(line)
        m = re.findall(r"per_page=\d+",response.url)
        if (m):
            m = re.findall(r"\d+", response.url)
            m = int(m[0]) + 15
            m = "per_page=" + str(m)
            url = re.sub(r"per_page=\d+", m, response.url)
        else:
            url = re.sub(r"topic\?", r"topic?per_page=15&", response.url)
        if not (response.xpath('//div[@class="pagina"]//a').extract()[-1] == response.xpath('//div[@class="pagina"]//a[@class="active"]').extract_first()):
            yield scrapy.Request(url, callback=self.parse)
