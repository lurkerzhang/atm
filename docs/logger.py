#!_*_coding:utf-8 _*_
# __author__:"lurkerzhang"

import logging
import os.path
import time
# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log level
# 创建handler，用于写入日志文件,每小时的保存到一个日志里面
rq = time.strftime('%Y%m%d%H', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/log/'
log_name = log_path + rq + '.log'
logfile = log_name
fh = logging.FileHandler(logfile, mode='a')
fh.setLevel(logging.DEBUG)  # 输出到file的log level
# 定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 将logger添加到handler
logger.addHandler(fh)
# 写日志样例
# logger.debug('this is a logger debug message')
# logger.info('this is a logger info message')
# logger.warning('this is a logger warning message')
# logger.error('this is a logger error message')
# logger.critical('this is a logger critical message')