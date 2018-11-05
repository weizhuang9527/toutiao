# -*- coding: utf-8 -*-
#
# @Author : ccl
# @Time : 2018/9/30 16:13
# --------------------------------------
from exts import db
from datetime import datetime


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(60))
    type = db.Column(db.String(10))
    source = db.Column(db.String(20))
    url = db.Column(db.String(255))
    # 是否已用 0未用 1已用
    used = db.Column(db.Integer)
    # 文章发布时间戳
    publish_timestamp = db.Column(db.Integer)
    # 创建时间
    create_at = db.Column(db.DateTime, default=datetime.now)
    # 更新时间
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, article_dict):
        self.id = article_dict.get('item_id', None)
        # 标题
        self.title = article_dict.get('title', None)
        # gallery图集 video视频 article文章
        self.type = article_dict.get('article_genre', None)
        # 来源
        self.source = article_dict.get('source', None)
        self.url = article_dict.get('display_url', None)
        self.used = 0
        self.publish_timestamp = article_dict.get('behot_time', None)

    def pop(self):
        if self.id is None:
            return False
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def is_used(self):
        self.used = 1
        db.session.commit()

    def __repr__(self):
        return '<Article {}>'.format(self.id)


# 日志表
class Log(db.Model):
    __tablename__ = 'log'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 级别 DEBUG调试 INFO信息 WARN警告 ERROR异常
    level = db.Column(db.String(10), nullable=False)
    # 信息
    message = db.Column(db.Text(10), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)

    def add(self):
        db.session.add(self)
        db.session.commit()

# 更新数据库用这两条命令
# python manage.py db init
# python manage.py db migrate
# python manage.py db upgrade
