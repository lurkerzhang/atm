#!_*_coding:utf-8 _*_
# __author__:"lurkerzhang"

from docs.conf import DATABASE
from docs.conf import DBDIR
import json
import os.path
import os
logined = False


# 认证管理登陆
def auth(func):
    def wrapper(*args, **kw):
        global logined
        if logined:
            return func(*args, **kw)
        else:
            login()
            return func(*args, **kw)

    return wrapper


# 超级管理员登陆
def login():
    admin_list = get_db_dict()['super']
    global logined
    while True:
        print('管理员：')
        user = input()
        print('密 码：')
        pwd = input()
        for i in admin_list:
            if i['name'] == user and i['password'] == pwd:
                logined = True
                return True
            else:
                print('管理用户名或密码错误')


# 保存银行账户信息
@auth
def save_db_bank(bank_list):
    new_db_path = os.path.join(DBDIR, 'data1.json')
    with open(DATABASE, 'r', encoding='utf-8') as db:
        db_dict = json.load(db)
        db_dict['bank'] = bank_list
    with open(new_db_path, 'w', encoding='utf-8') as f:
        json.dump(db_dict, f)
    os.replace(new_db_path, DATABASE)


# 读取数据
def get_db_dict():
    with open(DATABASE, 'r', encoding='utf-8') as db:
        db_dict = json.load(db)
    return db_dict


# 打印菜单
def show_menu():
    menu = '''=====\033[1;33;44m 管理菜单 \033[0m======
    [1] 查看银行账户
    [2] 添加账户
    [3] 维护账户
    [4] 退出管理
    '''
    print(menu)


# 查看银行账户
def show_accounts(bank_list):
    print('     账号          余额        信用额度       可用额度       还款日      账户状态   ')
    for i in bank_list:
        line = '{:^14}{:^14}{:^14}{:^14}{:^14}{:^14}'.format(i['account'], i['balance'], i['max'], i['limit'],
                                                             i['repay_day'], i['status'])
        print(line)


# 添加账户
def add_account(bank_list):
    while True:
        account = input('账号(10位数字)：').strip()
        if account.isdigit() and len(account) == 10:
            account_exist = False
            for i in bank_list:
                if i['account'] == account:
                    account_exist = True
            if account_exist:
                print('卡号已存在')
                continue
            while True:
                password = input('密码（6位数字）：').strip()
                if password.isdigit() and len(password) == 6:
                    while True:
                        balance = input('账户余额：').strip()
                        if balance.isdigit():
                            balance = int(balance)
                            while True:
                                limit = input('信用卡额度：').strip()
                                if limit.isdigit():
                                    limit = int(limit)
                                    while True:
                                        repay_day = input('还款日：')
                                        if repay_day.isdigit():
                                            if 0 < int(repay_day) < 29:
                                                repay_day = int(repay_day)
                                                new_account = {'account': account, 'password': password, 'balance': balance,
                                                               'max':limit ,'limit': limit, 'repay_day': repay_day, 'status': 1,
                                                               'is_logined': False, 'record': []}
                                                bank_list.append(new_account)
                                                return bank_list
                                            else:
                                                print('还款日范围必须为1--28')
                                                continue
                                        else:
                                            print('还款日格式不对')
                                            continue
                                else:
                                    print('输入的额度格式不对')
                                    continue

                        else:
                            print('输入的余额格式不对')
                            continue
                else:
                    print('密码格式不对')
                    continue
        else:
            print('卡号格式不对')
            continue


# 维护账号
def maintain(bank_list):
    while True:
        print('输入要修改的账号：')
        account = input().strip()
        account_exist = False
        index = 0
        for i in bank_list:
            if i['account'] == account:
                account_exist = True
                while True:
                    print('''[1]:重置信用额度\n[2]:账户状态修改\n[3]退出修改''')
                    s = input('>>>').strip()
                    if s == '1':
                        while True:
                            print('输入新信用额度：')
                            limit = input().strip()
                            if limit.isdigit():
                                limit = int(limit)
                                i['max'] = limit
                                i['limit'] = limit
                                print('账户：%s 的额度成功修改为%s' % (i['account'],i['limit']))
                                break
                            else:
                                print('额度格式输入错误')
                    elif s == '2':
                        while True:
                            print('输入冻结状态（1为正常，2为暂时限制，3为永久冻结）：')
                            status = input().strip()
                            if status in ['1','2','3']:
                                status = int(status)
                                i['status'] = status
                                print('账户：%s 的状态修改成功' % i['account'])
                                break
                            else:
                                print('输入错误！')
                                continue
                    elif s == '3':
                        bank_list[index] = i
                        return bank_list
                    else:
                        print('输入错误')
            index +=1
        if not account_exist:
            print('卡号不存在')
            continue
        return bank_list


@auth
def super_admin():
    db_dict = get_db_dict()
    bank_list = db_dict['bank']
    while True:
        show_menu()
        print('选择>>>')
        s = input().strip()
        if s == '1':
            show_accounts(bank_list)
        elif s == '2':
            bank_list = add_account(bank_list)
        elif s == '3':
            bank_list = maintain(bank_list)
        elif s == '4':
            save_db_bank(bank_list)
            exit('退出ATM超级管理员系统，再见！')
        else:
            print('输入错误')


if __name__ == '__main__':
    super_admin()
