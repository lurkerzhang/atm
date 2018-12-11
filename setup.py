#!_*_ coding:utf-8 _*_
# __author__:"lurkerzhang"
import json
import os

db = {
    'users': [['aric', '123456'],
              ['alex', '123456'],
              ['shanshan', '123456'],
              ['zhang', '123456']],
    'goods': [{'name': '电脑', 'price': 1999},
              {'name': '鼠标', 'price': 10},
              {'name': '游艇', 'price': 20},
              {'name': '美女', 'price': 998},
              {'name': '手机', 'price': 3000},
              {'name': '相机', 'price': 19000},
              {'name': '冰箱', 'price': 5000}],
    'bank': [
        {'account': '0123456789',  # 假设借记卡和信用卡为同一个卡号account
         'password': '123456',
         'is_logined': False,
         'balance': 100000,  # 借记卡余额
         'max': 15000,  # 最大额度
         'limit': 15000,  # 可用信用额度
         'repay_day': 18,  # 信用卡还款日
         'status': 1,  # 账户状态 1为正常，2为限制使用，3为永久冻结
         'record': [],
         },
        {'account': '1122334455',  # 假设借记卡和信用卡为同一个卡号account
         'password': '123456',
         'is_logined': False,
         'balance': 100000,  # 借记卡余额
         'max': 15000,  # 最大额度
         'limit': 15000,  # 可用信用额度
         'repay_day': 18,  # 信用卡还款日
         'status': 1,  # 账户状态 1为正常，2为限制使用，3为永久冻结
         'record': [],
         },
    ],
    'super': [{'name': 'admin', 'password': 'admin'}]
}


def db_init(dic):
    if not os.path.exists('db'):
        os.mkdir('db')
    with open('db/data.json', 'w', encoding='utf-8') as f:
        json.dump(dic, f)


if __name__ == '__main__':
    db_init(db)
