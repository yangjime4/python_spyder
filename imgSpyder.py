# -*- coding: utf-8 -*-
import urllib2
from lxml import etree
import os

def getImgUrlByProductId(productId):
    url = "http://www.yiwugo.com/product/detail/"+str(productId)+".html"
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    
    html = etree.HTML(res)
    urlList = html.xpath("//span[@class='view_tem_bigimg']/a/@href")
    if (len(urlList)<1):
        print productId
        return None
    return  urlList[0]

def getImgUrlListByProductList(productList):
    urlList=[]
    for productId in productList:
        #print productId
        urlList.append(getImgUrlByProductId(productId))
    return urlList
        
def downloadImg(urlList,downloadPath,keyword):
    imgName ="img"
    imgIndex=1
    finalPath =downloadPath+keyword+"\\" 
    for imgPath in urlList:
        print(imgPath)
        if not os.path.exists(finalPath):
            os.mkdir(finalPath)
        with open(finalPath+imgName+str(imgIndex)+".jpg","wb") as f: #开始写文件，wb代表写二进制文件
            f.write((urllib2.urlopen(imgPath)).read())                    
        imgIndex += 1
        
#通过中文词获取图片url列表        
def getTaobaoImgUrlsByWord(word):
    url = "https://s.taobao.com/search?q="+word
    req = urllib2.Request(url)
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    print req
#    html = etree.HTML(res)
#    print html
#    #urlList = html.xpath("//div[@class='pic-box-inner']/div[@class='pic']/a/img/@src")
#    urlList = html.xpath("//div[@class='pic-box-inner']")
#    return  urlList[0]


#print getImgUrlListByProductList(["926511158","929150939","929157264"])
#path="C:\Users\Administrator\Desktop\python http\img\\"        
#downloadImg(getImgUrlListByProductList(["926511158","929150939","929157264"]),path,"00001") 
        
        
#path="C:\Users\Administrator\Desktop\python http\img\\"
#downloadImg(getImgUrlListByProductList(["926511158","929150939","929157264"]),path,"80080101010000")
    
print getTaobaoImgUrlsByWord("skill")
        
            