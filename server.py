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


@app.route('/')
def index():
    return 'Welcome to ccl server'


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
    three_min_time = now - timedelta(minutes=10)
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

@app.route('/api/message/unread')
def api_getlist():
    data = {
        "state": 1,
        "msg": "获取数据成功",
        "data": {
            "count": 74,
            "list": [{
                "id": 1658,
                "title": "文章<我艹你奶奶个腿>审核未通过，文章<我艹你奶奶个腿>审核未通过",
                "url": "/message/1658"
            }, {
                "id": 1653,
                "title": "文章完结通知",
                "url": "/message/1653"
            }, {
                "id": 1621,
                "title": "文章完结通知",
                "url": "/message/1621"
            }, {
                "id": 1623,
                "title": "文章完结通知",
                "url": "/message/1623"
            }, {
                "id": 1580,
                "title": "文章完结通知",
                "url": "/message/1580"
            }]
        }
    }
    return jsonify(data)


@app.route('/api/task/manage/list')
def writer_getlist():
    data = {
        "state": 1,
        "msg": "获取数据成功",
        "data": {
            "count": 74,
            "list": [{
                "id": "1658",  # 任务单ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-11-02 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "ready",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": ""  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价回收旧电脑洗衣机电饭煲冰箱彩电游戏机",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            },{
                "id": "1658",  # 任务单ID
                "title": "高价回收旧电脑洗衣机电饭煲冰箱彩电游戏机",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "end_at": "2018-10-28 12:00:01",  # 结束时间
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658",  # 任务具体地址
                "status": "save",  # 状态 ready准备期 save保存 review提交审核中 pass通过完结 edit撤回修改 refuse拒绝
                "article_id": "10313"  # 对应文章ID ready准备期没有文章ID
            }]
        }
    }
    time.sleep(1)
    return jsonify(data)


@app.route('/api/task/platform/list')
def writer_platform_getlist():
    data = {
        "state": 1,
        "msg": "获取数据成功",
        "data": {
            "count": 74,
            "list": [{
                "id": "1658",  # 任务ID
                "title": "高价收历史文章 1元/100字",  # 任务标题
                "tags": ["字数:100", "领域:历史"],  # 任务标签
                "cut_off_at": "2018-10-28 12:00:01",  # 截止时间
                "still_need_num":3,  # 还需求篇数
                "point": 114,  # 积分 已扣抽成后
                "point_deposit": 12,  # 押金 积分*0.1 向上取整
                "url": "/message/1658"  # 任务具体地址
            }]
        }
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=33301)
