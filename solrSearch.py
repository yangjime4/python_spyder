# -*- coding: utf-8 -*-
import urllib2
import json 
import jsonpath

#测试
#server = "10.6.62.226:8981"
#正式
server = "10.3.3.104:8981"

#通过词码获取产品id列表
def getProductIdsByWordCode(wordCode): 
    url = "http://"+server+"/solr/newproduct/select?q=dissimilarity%3A*"+wordCode+"%3D8*&wt=json&indent=true"
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    jsonobj = json.loads(res)
    productList =jsonpath.jsonpath(jsonobj, '$..docs[*].id')    
    return productList




print getProductIdsByWordCode("80090203000000")
    
    
    

