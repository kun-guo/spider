# encoding: utf-8

import scrapy
import urlparse
import time
import re
from Spider.items import DmozItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["58.com"]
    start_urls = [
        "http://gz.58.com/job.shtml?PGTID=0d000000-0000-078d-3902-cd2755ebc698&ClickID=1",
        "http://cd.58.com/job.shtml?PGTID=0d100000-0006-63b2-e51e-49068eed0838&ClickID=2",
        "http://cs.58.com/job.shtml?PGTID=0d100000-0019-e153-33cf-77168b039a67&ClickID=2",
        "http://wh.58.com/job.shtml?PGTID=0d100000-0009-e2a1-f4af-9e61b6791f48&ClickID=2",
        "http://sh.58.com/job.shtml?PGTID=0d100000-0000-20d2-722d-84b0e4c9b923&ClickID=2",
        "http://sz.58.com/job.shtml?PGTID=0d100000-0000-4085-64c0-ba6a0abc67ec&ClickID=2",
        "http://bj.58.com/job.shtml?PGTID=0d100000-0000-1fdf-657d-9853fa3616c5&ClickID=1",
        "http://hz.58.com/job.shtml?PGTID=0d100000-0000-2693-daf6-f50e7c88f7d1&ClickID=1"
    ]

    city_map = {"sh": u"上海", "sz": u"深圳", "hz": u"杭州",
                "bj": u"北京", "cs": u"长沙", "wh": u"武汉", "cd": u"成都", "gz": u"广州"}

    def parse(self, response):
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
