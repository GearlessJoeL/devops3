#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by imoyao at 2019/6/24 9:37
"""
定义所有需要用到的表结构
"""
from datetime import datetime

from flask import current_app, Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context

#from back.exception import ValidationError

db = SQLAlchemy()

class User(db.Model):
    """
    用户表结构
    """
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    # 因为有用户名登录选项，所以此处必须唯一
    username = db.Column(db.String(64), index=True, unique=True, comment='用户名')
    password = db.Column(db.String(128), comment='密码，加密保存')
    email = db.Column(db.String(64), index=True, unique=True, comment='邮箱')
    character = db.Column(db.Integer, comment='用戶角色, 0为普通用户, 1为管理员')
    devices = db.relationship('Device')

    def __repr__(self):
        return '<User %r>' % self.username

    def hash_password(self, password):
        """
        密码加密
        :param password:原始密码
        :return:
        """
        self.password = custom_app_context.encrypt(password)
        return self.password

    def verify_user_password(self, password):
        """
        验证密码
        :param password:str,原始密码
        :return:bool
        """
        return custom_app_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        """
        生成token，有效时间10min  >> 10*60
        :param expiration:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """
        使用token方式认证，解析token，确认登录的用户身份
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        # 根据username查询，查到则认证通过，否则校验失败
        username = data.get('username')
        user = User.query.filter(or_(User.username == username, User.email == username)).one_or_none()
        # user = User.query.get(data['id'])
        return 
        
    
    @staticmethod
    def init_db():
        test_users = [(10, 'admin', '06153019', '010414@163.com', 1), (11, 'test_user1', '1101011953', 'xgp@163.com', 0), (12, 'test_user2', '19930717', 'tytx@163.com', 0)]
        for line in test_users:
            p = User()
            p.id = line[0]
            p.username = line[1]
            p.password = line[2]
            p.email = line[3]
            p.character = line[4]
            db.session.add(p)
        db.session.commit()


class Device(db.Model):
    """
    设备表结构
    """
    __tablename__ = 'device'
    __table_args__ = {'extend_existing': True}
    device_id = db.Column(db.String(32), primary_key=True, comment='设备唯一序列号')
    device_name = db.Column(db.String(128), unique=False, comment='设备名称')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), comment='用户id')
    device_temperature = db.Column(db.Integer, unique=False, comment='设备温度')
    device_humidity = db.Column(db.Integer, unique=False, comment='设备湿度')
    '''
    # https://stackoverflow.com/questions/36225736/flask-sqlalchemy-paginate-over-objects-in-a-relationship
    # http://www.pythondoc.com/flask-sqlalchemy/models.html#one-to-many
    # https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#many-to-many
    # https://stackoverflow.com/questions/23469093/flask-sqlalchemy-query-in-a-many-to-many-itself-relationship
    
    backref 和 lazy 意味着什么了？backref 是一个在 Address 类上声明新属性的简单方法。您也可以使用 my_address.person 来获取使用该地址(address)的人(person)。
    lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据:
    'select' (默认值) 就是说 SQLAlchemy 会使用一个标准的 select 语句必要时一次加载数据。
    'joined' 告诉 SQLAlchemy 使用 JOIN 语句作为父级在同一查询中来加载关系。
    'subquery' 类似 'joined' ，但是 SQLAlchemy 会使用子查询。
    'dynamic' 在有多条数据的时候是特别有用的。不是直接加载这些数据，SQLAlchemy 会返回一个查询对象，在加载数据前您可以过滤（提取）它们。
    您如何为反向引用（backrefs）定义惰性（lazy）状态？使用 backref() 函数:
    '''
    users = db.relationship('User', back_populates='devices')

    def __repr__(self):
        return '<Article %r>' % self.title

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise 'post dose not have a body.'
        return Device(body=body)

    @staticmethod
    def init_db():
        test_devices = [('19700101', 'device1', 11, 25, 85), ('19700102', 'device2', 12, 15, 75), ('19700103', 'device3', 11, 5, 65)]
        for line in test_devices:
            p = Device()
            p.device_id = line[0]
            p.device_name = line[1]
            p.user_id = line[2]
            p.device_temperature = line[3]
            p.device_humidity = line[4]
            db.session.add(p)
        db.session.commit()


# if __name__ == '__main__':
