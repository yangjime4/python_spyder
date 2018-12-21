# -*- coding: utf-8 -*-
import urllib2
from lxml import etree
import os


class ImgSpider:

    def __init__(self):
        pass

    @staticmethod
    def get_img_url_by_product_id(product_id):
        url = "http://www.yiwugo.com/product/detail/" + str(product_id) + ".html"
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()

        html = etree.HTML(res)
        url_list = html.xpath("//span[@class='view_tem_bigimg']/a/@href")
        if len(url_list) < 1:
            #print product_id
            return None
        return url_list[0]

    def get_img_url_list_by_product_list(self, product_list):
        url_list = []
        for productId in product_list:
            # print productId
            url_list.append(self.get_img_url_by_product_id(productId))
        return url_list

    @staticmethod
    def download_img(url_list, download_path, product_list, word_code):
        img_index = 0
        final_path = download_path + "\\" + word_code + "\\"
        for imgPath in url_list:
            # print(imgPath)
            if not os.path.exists(final_path):
                os.mkdir(final_path)
            with open(final_path + str(product_list[img_index]) + ".jpg", "wb") as f:  # 开始写文件，wb代表写二进制文件
                f.write((urllib2.urlopen(imgPath)).read())
            img_index += 1
            if img_index == len(url_list)-1:
                with open(final_path + "end.txt", "wb") as f:
                    f.write("end.txt")

    # 通过中文词获取图片url列表
    @staticmethod
    def get_taobao_img_urls_by_word(word):
        url = "https://s.taobao.com/search?q=" + word
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        html = etree.HTML(res)
        # print html
        # urlList = html.xpath("//div[@class='pic-box-inner']/div[@class='pic']/a/img/@src")
        url_list = html.xpath("//div[@class='pic-box-inner']")
        return url_list[0]

    # print getImgUrlListByProductList(["926511158","929150939","929157264"])
    # path="C:\Users\Administrator\Desktop\python http\img\\"
    # downloadImg(getImgUrlListByProductList(["926511158","929150939","929157264"]),path,"00001")

    # path="C:\Users\Administrator\Desktop\python http\img\\"
    # downloadImg(getImgUrlListByProductList(["926511158","929150939","929157264"]),path,"80080101010000")
