# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, Response
import os
from nt import chdir
# myPackage
from img_spider import ImgSpider
from solr_search import SolrSearch

executor = ThreadPoolExecutor(1)
app = Flask(__name__)
imgs_path = 'C:\PycharmProjects\python_spider\img'


# 1.通过词码获取产品列表
@app.route('/getProdList/<word_code>')
def get_prod_list(word_code):
    product_list = SolrSearch.get_product_ids_by_word_code(word_code)
    return str(product_list)


# 2.下载词码对应的产品列表的主图
@app.route('/downloadImgs/<word_code>')
def download_imgs(word_code):
    # 判断是否已下载完
    if os.path.exists(imgs_path + '\\' + word_code + '\\' + 'end.txt'):
        return '下载完成'
    else:
        executor.submit(start_download_imgs, word_code)
        return '正在下载'


def start_download_imgs(word_code):
    product_list = SolrSearch.get_product_ids_by_word_code(word_code)
    img_spider = ImgSpider()
    img_url_list = img_spider.get_img_url_list_by_product_list(product_list)
    ImgSpider.download_img(img_url_list, imgs_path, product_list, word_code)


# 3.通过词码获取已下载的图片列表
@app.route('/rawImgs/<word_code>')
def get_raw_imgs(word_code):
    path = imgs_path + '\\' + word_code
    dirs = os.listdir(path)
    files = []
    for i in dirs:
        if os.path.splitext(i)[1] == ".jpg":
            files.append(i)
    return files


# 4.通过词码.图片名获取图片
@app.route("/getRawImg/<word_code>/<img_name>")
def get_raw_img(word_code, img_name):
    image = file(imgs_path + "/{word_code}/{img_name}".format(word_code=word_code, img_name=img_name), 'rb')
    resp = Response(image, mimetype="image/jpeg")
    return resp


# 5.收集人工过滤后的图片数据
@app.route("/collectImgs/<word_code>/<img_names>")
def post_collected_imgs(word_code, img_names):
    path = imgs_path + '\\' + word_code
    path_filter = imgs_path + '\\' + word_code + '_filter'
    for img in img_names:
        if not os.path.exists(path + '\\' + img):
            return 'false'
    try:
        # 如果路径不存在，创建路径
        if not os.path.exists(path_filter):
            os.makedirs(path_filter)
        for img in img_names:
            path1 = path + '\\' + img
            path2 = path_filter + '\\' + img
            print(path1)
            print(path2)
            os.rename(path1, path2)
        return 'true'
    except:
        return 'false'


# 6.获取过滤后的图片列表
@app.route("/filterImgs/<word_code>")
def get_filter_imgs(word_code):
    path = imgs_path + '\\' + word_code + '_filter'
    print(path)
    dirs = os.listdir(path)
    files = []
    for i in dirs:
        if os.path.splitext(i)[1] == ".jpg":
            files.append(i)
    return files


# 7.获取过滤后的图片
@app.route("/getFilterImg/<word_code>/<img_name>")
def get_filter_img(word_code, img_name):
    path = imgs_path + '\\' + word_code + '_filter\\' + img_name
    print(path)
    image = file(path, 'rb')
    resp = Response(image, mimetype="image/jpeg")
    return resp

# 8.训练图片分类器，并部署到生产环境
# TODO
# @app.route("/train/<word_code_list")
# def train_by_word_code(word_code_list):
#
#     for word_code in word_code_list:


def regression_test(word_code):
    # interface1-7
    assert (get_prod_list(word_code) is not None)

    assert (download_imgs(word_code) == '下载完成')

    assert (get_raw_imgs(word_code) is not None)

    assert (get_raw_img(word_code, '923310729.jpg') is not None)


if __name__ == '__main__':
    # regression_test('80090404040102')
    # app.run(host='127.0.0.1', port='5000', debug=0)
    print(get_filter_img('80090404040102', '923363698.jpg'))