#!_*_coding:utf-8 _*_
# __author__:"lurkerzhang"
from docs.conf import DATABASE
import json


# 认证登陆状态
def auth(func):
    def wrapper(*args, **kw):
        if args[0].get('is_logined'):
            return func(*args, **kw)
        else:
            temp = list(args)
            temp[0] = login()
            args = tuple(temp)
            return func(*args, **kw)

    return wrapper


def get_usd():
    with open(DATABASE, 'r', encoding='utf-8') as db:
        db_dict = json.load(db)
    return db_dict.get('users')


# 用户登陆
def login():
    usd = get_usd()
    while True:
        print('输入用户名：')
        username = input()
        print('输入密码：')
        password = input()
        for i in usd:
            if i[0] == username and i[1] == password:
                print('登陆成功！')
                me_data = {'name': i[0], 'is_logined': True, 'shopping_cart': {'goods': {}, 'money': 0},'shopping_record':[]}
                return me_data
        else:
            print('账号或密码错误')
