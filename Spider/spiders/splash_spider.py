# encoding: utf-8

import scrapy
import urlparse
import time
import re
from Spider.items import DmozItem
from scrapy_splash import SplashRequest


class DmozSpider(scrapy.Spider):
    name = "splash_spider"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://baidu.com"
    ]

    city_map = {"sh": u"上海", "sz": u"深圳", "hz": u"杭州",
                "bj": u"北京", "cs": u"长沙", "wh": u"武汉", "cd": u"成都", "gz": u"广州"}

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        print response.body
        # 获取原始url的base url 与分类path 组合成分类地址
        url = response.url
        ret = urlparse.urlparse(url)
        base_url = ret.scheme + "://" + ret.netloc

        base_paths = response.xpath(
            '//a[@leibie]/@href').extract()

        print "=============分类路径==============".decode("utf-8")
        # 每个类别产生一个url抓取每个类别数据
        for path in base_paths:
            category_url = base_url + path
            print "分类地址:".decode("utf-8") + category_url

            request = scrapy.Request(
                category_url, dont_filter=True, callback=self.parse_categories)
            # request.meta['PhantomJS'] = False

            yield request

    def parse_categories(self, response):
        try:
            total_page = response.xpath(
                '//div[@class="pagesout"]/span[@class="num_operate"]/i/text()').extract_first()

            if total_page is None:
                return

            total_page = int(total_page)

            category_url = response.url + "/pn{0}/"

            for page in range(1, total_page):
                page_url = category_url.format(page)
                # print "分页地址:".decode("utf-8") + page_url

                request = scrapy.Request(
                    page_url, dont_filter=True, callback=self.parse_content)
                # request.meta['PhantomJS'] = True

                yield request

        except Exception, e:
            raise e

    def parse_content(self, response):
        # 获取城市

        city = response.xpath(
            '//div[@class="bar_left"]/h2/text()').extract_first()
        # print "解析城市 ========== ".decode("utf-8")
        # print city

        if(city is None):
            url = response.url
            ret = urlparse.urlparse(url)
            city_word = ret.netloc.split(".")[0]
            city = self.city_map[city_word]

        for sel in response.xpath('//li[@class="job_item clearfix"]'):

            district = sel.xpath(
                'div[@class="item_con job_title"]/div[@class="job_name clearfix"]/a/span[@class="address"]/text()').extract_first()
            try:
                district = re.sub(r"\r|\n|\t|\s", "", district)
            except Exception as err:
                print district
                print err

            job_salary = sel.xpath(
                'div[@class="item_con job_title"]/p[@class="job_salary"]/text()').extract_first()
            company = sel.xpath(
                'div[@class="item_con job_comp"]/div/a/@title').extract_first()

            title = sel.xpath(
                'div[@class="item_con job_comp"]/p[@class="job_require"]/span[@class="cate"]/text()').extract_first()
            edu = sel.xpath(
                'div[@class="item_con job_comp"]/p[@class="job_require"]/span[@class="xueli"]/text()').extract_first()
            exp = sel.xpath(
                'div[@class="item_con job_comp"]/p[@class="job_require"]/span[@class="jingyan"]/text()').extract_first()

            item = DmozItem()
            item["city"] = city
            item["district"] = district
            item["job_salary"] = job_salary
            item['company'] = company
            item['title'] = title
            item['edu'] = edu
            item['exp'] = exp
            item['come_from'] = u"1"

            yield item
