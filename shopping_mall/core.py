#!_*_coding:utf-8 _*_
# __author__:"lurkerzhang"
from shopping_mall.login_auth import auth
from docs.conf import DBDIR, DATABASE
import os, os.path
import json
from atm.core import pay
import time


# 读取数据库
@auth
def get_db_dic(me_data):
    with open(DATABASE, 'r', encoding='utf-8') as db:
        db_dict = json.load(db)
    return [me_data, db_dict]


# 保存用户历史数据
@auth
def save_data(me_data):
    user = me_data.get('name')
    me_data['is_logined'] = False
    user_db_path = os.path.join(DBDIR, user)
    f = open(user_db_path, 'w', encoding='utf-8')
    f.write(str(me_data))
    f.close()


# 读用户历史数据
@auth
def history(me_data):
    user = me_data.get('name')
    user_db_path = os.path.join(DBDIR, user)
    try:
        with open(user_db_path, 'r', encoding='utf-8') as f:
            d = f.read()
            if d:
                usd = eval(d)
            else:
                usd = {}
    except FileNotFoundError:
        # 如果文件不存在就创建
        with open(user_db_path, 'w') as f:
            usd = {}
    return usd


# 打印商品
def show_goods(goods):
    print('''=====\033[1;33;44m 商品列表 \033[0m=====
序号   名称    价格''')
    for i in range(1, len(goods) + 1):
        print(' %s     %s    %s' % (i, goods[i - 1]['name'], goods[i - 1]['price']))


# 打印主菜单
def show_menu():
    print('''
=====\033[1;33;44m 选择菜单 \033[0m======
[A]----------->显示商品列表
[B]----------->查看购物车
[C]----------->选购商品
[D]----------->购买记录
[E]----------->去结算
[Q]----------->退出 ''')


# 打印购物车
def show_cart(me_data):
    cart = me_data.get('shopping_cart')
    if not cart.get('goods'):
        print('购物车为空！')
    else:
        print("=======\033[1;33;44m 购物车 \033[0m=======")
        for name, amount in cart['goods'].items():
            print('商品名称：%s，数量：%s' % (name, amount))
        print('购物车总金额：%s' % cart['money'])


# 打印购买记录
def show_record(record):
    if not record:
        print('购物车记录为空')
    else:
        print('=====================\033[1;33;44m 购买记录 \033[0m==================')
        for i in record:
            print('购买时间：%s' % i['time'])
            for name, count in i['goods']['goods'].items():
                print('    商品名称：%s,数量：%s' % (name, count))
            print('    消费金额：%s元' % i['goods']['money'])


# 购买商品
@auth
def buy(me_data, goods, me):
    while True:
        print("请输入需要购买的商品ID【B:去主菜单；Q:退出程序】；E:去结算")
        to_buy = input()
        try:
            to_buy = int(to_buy) - 1
        except Exception:
            if to_buy.strip().upper() == "B":
                return me_data
            elif to_buy.strip().upper() == "E":
                _account = {'account': '', 'password': '', 'balance': 0, 'limit': 0, 'repay_day': 0, 'status': 0,'is_logined': False}
                me_data = to_pay(_account, me_data)
                return me_data
            elif to_buy.strip().upper() == "Q":
                show_cart(me_data)
                save_data(me_data)
                exit()
        if to_buy not in list(range(len(goods))):
            print('输入错误')
            continue
        else:
            if goods[to_buy]['name'] in me_data['shopping_cart']['goods'].keys():
                # 如果购物车已经有了该商品，数量加1
                me_data['shopping_cart']['goods'][goods[to_buy]['name']] += 1
            else:
                me_data['shopping_cart']['goods'][goods[to_buy]['name']] = 1
            me_data['shopping_cart']['money'] += goods[to_buy]['price']
            print('\033[1;33;44m 成功加入购物车：%s 1件  !\033[0m' % (goods[to_buy]['name']))


def run():
    me_data = {'name': '', 'is_logined': False, 'shopping_cart': {'goods': {}, 'money': 0}}
    data = get_db_dic(me_data)
    me_data = data[0]

    goods = data[1]['goods']
    me = me_data.get('name')
    # 尝试读取用户历史信息
    last_data = history(me_data)
    if last_data:
        print('欢迎你，%s，你的购物车有商品，可继续购买或直接结算' % me)
        # 老用户直接加载历史数据
        me_data['shopping_cart'] = last_data['shopping_cart']
        me_data['shopping_record'] = last_data['shopping_record']
    else:
        print('欢迎你，%s，你购物车为空，请添加商品到购物车再结算' % me)
    # 展示所有商品信息
    show_goods(goods)
    me_data = buy(me_data, goods, me)
    while True:
        # 打印选择菜单
        show_menu()
        print('你的选择：')
        s = input()
        if s.strip().upper() == "Q":
            show_cart(me_data)
            save_data(me_data)
            print("退出购物商城，再见！")
            exit()
        elif s.strip().upper() == "A":
            show_goods(goods)
        elif s.strip().upper() == "B":
            show_cart(me_data)
        elif s.strip().upper() == 'C':
            me_data = buy(me_data, goods, me)
        elif s.strip().upper() == 'D':
            show_record(me_data['shopping_record'])
        elif s.strip().upper() == "E":
            _account = {'account': '', 'password': '', 'balance': 0, 'limit': 0, 'repay_day': 0, 'status': 0,
                        'is_logined': False}
            me_data = to_pay(_account, me_data)
        else:
            print('输入错误！请重新输入：')


# 商品结算
def to_pay(my_account, me_data):
    money = me_data['shopping_cart']['money']
    if me_data['shopping_cart']['goods']:
        print('验证结算的信用卡：')
        pay_result = pay(my_account, money)
        if pay_result:
            # 获取购买当前时间
            now = time.asctime(time.localtime(time.time()))
            rd = {'time': now, 'goods': me_data['shopping_cart']}
            me_data['shopping_record'].append(rd)
            # 结算成功后清空购物车
            me_data['shopping_cart'] = {'goods': {}, 'money': 0}
        else:
            print('结算失败')
    else:
        print('购物车为空，无法结算。')
    return me_data
