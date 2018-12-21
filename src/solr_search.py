# -*- coding: utf-8 -*-
import urllib2
import json
import jsonpath

# 测试
# server = "10.6.62.226:8981"
# 正式
server = "10.3.3.104:8981"


class SolrSearch:

    def __init__(self):
        pass

    # 通过词码获取产品id列表
    @staticmethod
    def get_product_ids_by_word_code(word_code):
        url = "http://" + server + "/solr/newproduct/select?q=dissimilarity%3A*" + word_code + "%3D8*&wt=json&indent=true"
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        res = res_data.read()
        json_obj = json.loads(res)
        product_list = jsonpath.jsonpath(json_obj, '$..docs[*].id')
        return product_list


if __name__ == '__main__':
    print SolrSearch.get_product_ids_by_word_code()
