# -*- coding: utf-8 -*-
# 文章库
# @Author : ccl
# @Time : 2018/9/30 14:58
# --------------------------------------
from flask import Flask, request, jsonify
import config
from flask_cors import *
from exts import db
from models import Article
from datetime import datetime, timedelta
import time

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
CORS(app, supports_credentials=True)


def wrap_true(msg, data={}):
    return jsonify({
        "status": "success",
        "msg": msg,
        "data": data
    })


def wrap_false(msg):
    return jsonify({
        "status": "error",
        "msg": msg,
    })


@app.route('/test')
def test_view():
    return "11"


@app.route('/api/data', methods=['POST'])
def api_data_api():
    data = request.get_json()
    msg = data.get('message')
    if msg != "success":
        return wrap_false(msg="获取数据错误")
    article_list = data.get('data')

    count = len(article_list)
    if count == 0:
        return wrap_false(msg="获取到的数据为空")
    allow_num = 0
    for article in article_list:
        if Article(article).pop():
            allow_num += 1
            print('符合筛选要求,成功添加')
        else:
            print('未符合筛选要求')
    print("allow_num:{},count:{}".format(allow_num, count))
    point = allow_num / count
    print('总共：{} 成功{} 成功率{}'.format(count, allow_num, point))
    if point < 0.5:
        data = {
            "status": "end"
        }
        return wrap_true(msg="上传成功", data=data)
    data = {
        "status": "keep",
        "max_behot_time": data.get('next').get('max_behot_time')
    }
    return wrap_true(msg="继续上传", data=data)


@app.route('/api/get', methods=['GET'])
def api_get_api():
    now = datetime.now()
    three_min_time = now - timedelta(minutes=5)
    timestamp = int(time.mktime(three_min_time.timetuple()))
    # print(timestamp)
    article = Article.query.filter(Article.publish_timestamp > timestamp,
                                   Article.used == 0, Article.type == 'gallery').first()
    if not article:
        return wrap_false(msg='暂无文章')
    # print(article.publish_timestamp)
    # print(article.id)
    article.is_used()
    return wrap_true(msg='获取成功', data={"title": article.title, "url": article.url})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=33301, ssl_context='adhoc')
