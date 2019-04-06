# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapy.http import HtmlResponse
import time
import random


class PhantomJSMiddleware(object):

    @classmethod
    def process_request(cls, request, spider):

        if request.meta.has_key('PhantomJS'):
            print "=== 开始执行selenium请求网页 =====".decode("utf-8")
            driver = webdriver.PhantomJS()
            driver.get(request.url)

            driver.save_screenshot(
                "./img/" + str(random.randint(0, 100)) + 'screen.png')

            # 定位到要双击的元素
            #crumb_item = driver.find_element_by_xpath('//a[@leibie]/@href').extract_first()

            # 对定位到的元素执行鼠标双击操作
            # ActionChains(driver).click(crumb_item).perform()
            print "====== selenium请求网页完成 =====".decode("utf-8")

            content = driver.page_source.encode('utf-8')
            driver.quit()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)
