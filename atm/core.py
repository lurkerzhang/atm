#!_*_coding:utf-8 _*_
# __author__:"lurkerzhang"
from docs.conf import DATABASE, DBDIR, BASEDIR
import json
import os
from atm.bank_auth import auth
from atm.admin import super_admin
from docs.logger import *
import time

@auth
# 打印账户详情
def show_account(my_account):
    if my_account['status'] == 1:
        status = '正常使用'
    elif my_account['status'] == 2:
        status = '暂时限制'
    elif my_account['status'] == 3:
        status = '永久冻结'
    else:
        status = '未知状态'
    s = '''========\033[1;33;44m 账户信息 \033[0m========
    账    号： %s
    余    额： %s元
    信用额度： %s元
    可用额度： %s元
    还 款 日： 每月%s日
    账户状态： %s
    ''' % (
    my_account['account'], my_account['balance'], my_account['max'], my_account['limit'], my_account['repay_day'],
    status)
    print(s)
    return my_account


# 转账
@auth
def transfer(my_account):
    print('当前账号：%s  ;  余额：%s元' % (my_account['account'], my_account['balance']))
    print('输入转账账号>>>')
    transfer_account = input().strip()
    print('输入转账金额>>>')
    transfer_money = input().strip()
    if transfer_money.isdigit():
        transfer_money = float(transfer_money)
        if transfer_money > my_account['balance']:
            print('转账失败，余额不足！')
            return my_account
    else:
        print('输入错误')
        return my_account
    db = get_bank_list(my_account)
    my_account = db[0]
    bank_list = db[1]
    for i in range(len(bank_list)):
        if bank_list[i]['account'] == transfer_account:
            # 获取转账当前时间
            now = time.asctime(time.localtime(time.time()))
            rd1 = {'time': now, 'msg': '你向账号：%s 转账%s元' % (transfer_account, transfer_money)}
            rd2 = {'time': now, 'msg': '账号：%s 向你转账%s元' % (my_account['account'], transfer_money)}
            bank_list[i]['balance'] += transfer_money
            my_account['record'].append(rd1)
            bank_list[i]['record'].append(rd2)
            my_account['balance'] -= transfer_money
            print('你向账号：%s 转账%s元' % (transfer_account, transfer_money))
            save_account(bank_list[i])
            return my_account
    print('转账失败，转入账号不存在！')
    return my_account


# 还款
@auth
def repay(my_account):
    print('当前银行卡余额为：%s元，信用卡欠款：%s元' % (my_account['balance'], my_account['max']-my_account['limit']))
    if my_account['max'] == my_account['limit']:
        print('没有欠款，不用还！')
        return my_account
    else:
        while True:
            print('还款金额>>>')
            repay_money = input()
            if repay_money.isdigit():
                repay_money = float(repay_money)
                if repay_money > float(my_account['max'])-float(my_account['limit']):
                    print('还款太多了，没欠这么多钱！')
                    continue
                elif repay_money <=0:
                    print('输入错误')
                    continue
                elif repay_money > my_account['balance']:
                    print('余额不足')
                    continue
                else:
                    my_account['balance'] -= repay_money
                    my_account['limit'] += repay_money
                    # 获取转账当前时间
                    now = time.asctime(time.localtime(time.time()))
                    rd = {'time': now, 'msg': '你向信用卡账户：%s 还款%s元' % (my_account['account'], repay_money)}
                    my_account['record'].append(rd)
                    print('你向信用卡账户：%s 还款%s元' % (my_account['account'], repay_money))
                    if my_account['limit'] == my_account['max']:
                        print('恭喜你，已还清信用卡，当前额度为:%s元' % my_account['limit'])
                    else:
                        print('信用卡未还清，当前还欠款：%s元' % (float(my_account['max'])-float(my_account['limit'])))
                    return my_account
            else:
                print('输入错误！')
                continue


# 显示流水
@auth
def show_details(my_account):
    if len(my_account['record']):
        print('========\033[1;33;44m 账户流水 \033[0m========')
        for i in my_account['record']:
            print('%s  :   %s ' % (i['time'], i['msg']))
    else:
        print('账户流水为空！')
    return my_account


# 购物结算接口
@auth
def pay(my_account, money):
    if my_account.get('limit') >= money:
        my_account['limit'] -= money
        print('使用信用卡结算成功，当前信用卡额度还剩：%s元' % my_account.get('limit'))
        # 获取购买当前时间
        now = time.asctime(time.localtime(time.time()))
        rd = {'time': now, 'msg': '购物商场花费%s元' % money}
        my_account['record'].append(rd)
        save_account(my_account)
        return True
    else:
        print('结算失败，信息额度不够，当前信用卡额度还剩：%s元' % my_account.get('limit'))
        return False


# 保存账户数据
def save_account(my_account):
    account = my_account.get('account')
    my_account['is_logined'] = False
    # account_db_path = os.path.join(DBDIR, account)
    new_db_path = os.path.join(DBDIR, 'data1.json')
    with open(DATABASE, 'r', encoding='utf-8') as db:
        db_dict = json.load(db)
        for c in db_dict['bank']:
            if c.get('account') == account:
                db_dict['bank'][db_dict['bank'].index(c)] = my_account
    with open(new_db_path, 'w', encoding='utf-8') as f:
        json.dump(db_dict, f)
    os.replace(new_db_path, DATABASE)


# 连接银行数据库
@auth
def get_bank_list(my_acount):
    with open(DATABASE, 'r', encoding='utf-8') as db:
        db_dict = json.load(db)
    return [my_acount, db_dict.get('bank')]


# 打印菜单
def show_menu():
    print('''=====\033[1;33;44m ATM操作选项 \033[0m======
[A]----------->查看账户详情
[B]----------->转账
[C]----------->还款
[D]----------->购物
[E]----------->查看流水
[F]----------->查看日志
[G]----------->超级管理
[Q]----------->退出 ''')


# 读账户数据
def get_my_account(account):
    account_db_path = os.path.join(DBDIR, account)
    try:
        with open(account_db_path, 'r', encoding='utf-8') as f:
            d = f.read()
            if d:
                usd = eval(d)
            else:
                usd = {}
    except FileNotFoundError:
        # 如果文件不存在就创建
        with open(account_db_path, 'w', encoding='utf-8') as f:
            usd = {}
    return usd


def run():
    # 初始化用户数据
    my_account = {'account': '', 'password': '', 'balance': 0, 'limit': 0, 'repay_day': 0, 'status': 0,
                  'is_logined': False, 'record': []}
    my_account = get_bank_list(my_account)[0]
    logger.info('%s login in the atm.' % my_account['account'])
    while True:
        show_menu()
        print('选择>>>')
        s = input()
        if s.strip().upper() == "Q":
            logger.info('%s login out the atm.' % my_account['account'])
            save_account(my_account)
            print("退出ATM，再见！")
            exit()
        elif s.strip().upper() == "A":
            logger.info('%s print the account.' % my_account['account'])
            my_account = show_account(my_account)
        elif s.strip().upper() == "B":
            logger.info('%s try to transfer money.' % my_account['account'])
            my_account = transfer(my_account)
        elif s.strip().upper() == "C":
            logger.info('%s try to repay the credit.' % my_account['account'])
            my_account = repay(my_account)
        elif s.strip().upper() == "D":
            logger.info('%s go to the shopping mall.' % my_account['account'])
            shopping_mall_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                              'shopping_mall\main.py')
            os.system('python %s' % shopping_mall_path)
            # 重新读额度和流水
            for i in get_bank_list(my_account)[1]:
                if i['account'] == my_account['account']:
                    my_account['limit'] = i['limit']
                    my_account['record'] = i['record']
        elif s.strip().upper() == "E":
            logger.info('%s check the details.' % my_account['account'])
            my_account = show_details(my_account)
        elif s.strip().upper() == "F":
            logger.info('%s try to check the log file.' % my_account['account'])
            logs_dir = os.path.join(BASEDIR, 'log')
            os.system('explorer.exe /n, %s' % logs_dir)
        elif s.strip().upper() == "G":
            # 退出当前银行账户登陆状态
            save_account(my_account)
            print('退出atm用户系统，进入超级管理系统')
            super_admin()
        elif s.strip().upper() == "Q":
            save_account(my_account)
            exit('退出ATM用户操作系统，再见！')
        else:
            print('输入错误！')
