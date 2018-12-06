#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

# 用户登陆
def login(users):
    # 用户先登陆
    is_login = False
    while not is_login:
        try:
            with open('locked', 'r') as f:
                locked = f.read().splitlines()
        except FileNotFoundError:
            # 如果文件不存在就创建
            with open('locked', 'w') as f:
                locked = []

        # 提示用户输入用户名
        while True:
            user = input('用户名：').strip()
            if not user:
                print('用户名不能为空！')
                continue
            elif user in locked:
                return [user, False]
            else:
                is_user = []
                for i in users:
                    if i[0] == user:
                        is_user = i
                if not is_user:
                    print('用户不存在！')
                    continue
                else:
                    # 验证密码
                    count = 0
                    while count < 3:
                        # 提示输入用户名密码
                        pwd = input('密码：')
                        if pwd == is_user[1]:
                            return [is_user[0], True]
                        else:
                            print('密码错误！')
                            count += 1
                        if count == 3:
                            file = open('locked', 'a')
                            file.write('%s\n' % is_user[0])
                            file.close()
                            return [is_user[0], False]


# 读用户历史信息
def history(user):
    try:
        with open(user, 'r') as f:
            d = f.read()
            usd = eval(d)
    except FileNotFoundError:
        # 如果文件不存在就创建
        with open(user, 'w') as f:
            usd = {}
    return usd


# 打印商品
def show_goods(goods):
    print('''=====\033[1;33;44m 商品列表 \033[0m=====
序号   名称    价格''')
    for i in range(1, len(goods)+1):
        print(' %s     %s    %s' % (i, goods[i-1]['name'], goods[i-1]['price']))


# 打印主菜单
def show_menu():
    print('''
=====\033[1;33;44m 选择菜单 \033[0m======
[A]----------->商品列表
[B]----------->购物车
[C]----------->购买商品
[D]----------->购买记录
[E]----------->账户余额
[Q]----------->退出 ''')


# 打印购物车
def show_cart(cart):
    if not cart:
        print('什么都没购买！')
    else:
        print("=======\033[1;33;44m 购物车 \033[0m=======")
        for name, amount in cart.items():
            print('商品名称：%s，数量：%s' % (name, amount))


# 打印购买记录
def show_record(record):
    if not record:
        print('购买记录为空')
        print()
    else:
        print('=====================\033[1;33;44m 购买记录 \033[0m==================')
        for i in record:
            print('商品名称:%s   购买时间：%s' % (i['name'], i['time']))


# 保存数据
def save_data(data, user):
    f = open(user, 'w')
    f.write(str(data))
    f.close()


# 购买商品
def buy(me_data, goods, me):
    while True:
        print("请输入需要购买的商品ID【B:去主菜单；Q:退出程序】")
        to_buy = input()
        try:
            to_buy = int(to_buy)-1
        except Exception:
            if to_buy.strip().upper() == "B":
                show_cart(me_data['shopping_cart'])
                print('\033[1;35m 余额:%s元 \033[0m ' % me_data['salary'])
                return me_data
            elif to_buy.strip().upper() == "Q":
                show_cart(me_data['shopping_cart'])
                print('\033[1;35m 余额:%s元 \033[0m ' % me_data['salary'])
                save_data(me_data, me)
                exit()
        if to_buy not in list(range(len(goods))):
            print('输入错误')
            continue
        if me_data['salary'] < goods[to_buy]['price']:
            print('余额已不足，结束购买')
            return me_data
        else:
            if goods[to_buy]['name'] in me_data['shopping_cart'].keys():
                # 如果购物车已经有了该商品，数量加1
                me_data['shopping_cart'][goods[to_buy]['name']] += 1
            else:
                me_data['shopping_cart'][goods[to_buy]['name']] = 1
            # 获取购买当前时间
            now = time.asctime(time.localtime(time.time()))
            rd = {'name': goods[to_buy]['name'], 'time': now}
            me_data['shopping_record'].append(rd)
            me_data['salary'] -= goods[to_buy]['price']
            print('\033[1;33;44m 购买商品并成功加入购物车：%s 1件   余额：%s元 !\033[0m' % (goods[to_buy]['name'], me_data['salary']))


if __name__ == '__main__':
    # 读取文件数据
    f = open('data', 'r')
    data = f.read()
    data_dict = eval(data)
    f.close()
    users = data_dict['users']
    goods = data_dict['goods']

    login_result = login(users)
    if not login_result[1]:
        print('用户%s已被锁定无法登陆！' % login_result[0])
        exit()
    else:
        me = login_result[0]
        print('登陆成功！', end='')
        # 用户数据初始化
        me_data = {}
        # 尝试读取用户上次购物信息（购买的商品、余额、购买记录）
        last_data = history(me)
        if last_data:
            print('欢迎你，%s，你有购买记录，可继续购买' % login_result[0])
            # 老用户直接加载历史数据
            me_data['shopping_cart'] = last_data['shopping_cart']
            me_data['shopping_record'] = last_data['shopping_record']
            me_data['salary'] = last_data['salary']
        else:
            print('欢迎你，%s，你没有购买记录，输入工资后购买' % login_result[0])
            # 新用户提示输入工资
            salary = float(input("工资："))
            me_data['shopping_cart'] = {}
            me_data['shopping_record'] = []
            me_data['salary'] = salary

        # 展示所有商品信息
        show_goods(goods)
        me_data = buy(me_data, goods, me)
        while True:
            # 打印选择菜单
            show_menu()
            print('你的选择：')
            s = input()
            if s.strip().upper() == "Q":
                show_cart(me_data['shopping_cart'])
                print('\033[1;35m 余额:%s元 \033[0m ' % me_data['salary'])
                save_data(me_data, me)
                print("再见！")
                exit()
            elif s.strip().upper() == "A":
                show_goods(goods)
            elif s.strip().upper() == "B":
                show_cart(me_data['shopping_cart'])
            elif s.strip().upper() == 'C':
                me_data = buy(me_data, goods, me)
            elif s.strip().upper() == 'D':
                show_record(me_data['shopping_record'])
            elif s.strip().upper() == "E":
                print('\033[1;35m 余额:%s元 \033[0m ' % me_data['salary'])
            else:
                print('输入错误！请重新输入：')
