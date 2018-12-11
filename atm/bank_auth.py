#!_*_coding:utf-8 _*_
# __author__:"lurkerzhang"
from docs.conf import DATABASE
import json


# 认证银行账号登陆状态
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


def get_bank_db():
    with open(DATABASE, 'r', encoding='utf-8') as db:
        db_dict = json.load(db)
    return db_dict.get('bank')


# 银行账号登陆
def login():
    bank = get_bank_db()
    while True:
        print('输入卡号：')
        account = input()
        print('输入密码：')
        password = input()
        for i in bank:
            if i.get('account') == account and i.get('password') == password:
                my_account = i
                if my_account.get('status') == 2:
                    print('卡号被暂时限制，无法登陆')
                    exit()
                if my_account.get('status') == 3:
                    print('卡号被永久冻结，无法登陆')
                    exit()
                else:
                    my_account['is_logined'] = True
                    print('登陆成功！')
                    return my_account

        else:
            print('卡号或密码错误')