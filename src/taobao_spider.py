# -*- coding: utf-8 -*-
import requests
import json
import re
import time
import jsonpath


# jsonpath包地址 https://pypi.python.org/pypi/jsonpath
# jsonpath官方文档 http://goessner.net/articles/JsonPath


class TaoBaospider:
    def __init__(self):
        # cookie保持用于动态加载和分页，每次访问时更新
        self.cookies = ""

    # 通过url返回图片url
    def get_img_urls_by_url(self, url, pattern):
        content = ""
        success = False

        # 循环直到返回成功
        while not success:
            response = requests.get(url, cookies=self.cookies)
            self.cookies = response.cookies
            html = response.text
            success = False
            try:

                content = re.findall(pattern, html, re.S)[0].strip().strip(";")

                success = True
                time.sleep(1)
            except:
                success = False
        json_obj = json.loads(content)
        # 找到所有key为pic_url的value
        img_url_list = jsonpath.jsonpath(json_obj, '$..pic_url')
        return img_url_list

    # 通过关键词得到一页淘宝产品的图片
    def get_img_urls_page_by_word(self, word):
        url1 = 'https://s.taobao.com/search?q=' + word + '&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180430&ie=utf8'
        pattern1 = r'g_page_config = (.*?) g_srp_loadCss'
        urls = self.get_img_urls_by_url(url1, pattern1)

        url2 = 'https://s.taobao.com/api?_ksTS=1524836494360_224&callback=jsonp225&ajax=true&m=customized&sourceId=tb.index&q=' + word + '&spm=a21bo.2017.201856-taobao-item.1&s=36&imgfile=&initiative_id=tbindexz_20170306&bcoffset=-1&commend=all&ie=utf8&rn=efedc6cda629c8a38008aff6f017b934&ssid=s5-e&search_type=item'
        pattern2 = r'{.*}'
        urls = urls + self.get_img_urls_by_url(url2, pattern2)
        return urls

    # 翻页取产品 page_no取多少页 ，max_no最多取几个产品,返回产品图片url数组
    def get_img_urls_pages_by_word(self, word, page_no, max_no):
        urls = []
        for i in range(1, page_no):
            s = 44 * (i)
            url = "https://s.taobao.com/search?q=word={}&bcoffset=0&ntoffset=0&s=s={}".format(s, word)
            urls = urls + self.get_img_urls_by_url(url, r'g_page_config = (.*?) g_srp_loadCss')
            if (len(urls) > max_no):
                return urls[:max_no]
        return urls


if __name__ == '__main__':
    spider = TaoBaospider()
    urls = spider.get_img_urls_pages_by_word("毛巾", 50, 500)
    #print ("共有" + str(len(urls)) + "个图片")
    #print (urls)
