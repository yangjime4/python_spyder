# -*- coding: utf-8 -*-
from flask import Flask,Response

#myPackage
import solrSearch
import imgSpyder

app = Flask(__name__)

@app.route('/wordcode/<wordCode>')
def sendKeyword(wordCode): 
    productList = solrSearch.getProductIdsByWordCode(wordCode)
    imgUrlList = imgSpyder.getImgUrlListByProductList(productList)
    path="C:\Users\Administrator\Desktop\python http\img\\"
    imgSpyder.downloadImg(imgUrlList,path,wordCode)
    print imgUrlList               
    return '处理成功'

#wordCode为词码，imgId 为img1.jpg img2.jpg
@app.route("/img/<wordCode>/<imgId>")
def index(wordCode,imgId):
    image = file("img/{wordCode}/{imgId}".format(wordCode=wordCode,imgId=imgId),'rb')
    resp = Response(image, mimetype="image/jpeg")
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0')