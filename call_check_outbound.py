#!/usr/bin/python
# coding=utf-8

import sys
import time
import socket
import logging
import MySQLdb

import random
import hashlib
import requests

from datetime import datetime

# REDSMS var:
REDSMS_URL = 'https://cp.redsms.ru/api/message'
REDSMS_API_KEY = '52483a055a96d4e918fee0b8aed54f07fe06270e11'
REDSMS_LOGIN = 'lptracker'
REDSMS_ROUTE = 'sms'

# mysql connect param:
db_host = '127.0.0.1'
db_port = 3306
db_user = "root"
db_password = "dctvgfhjkm"
db_database = "alarm"

# Asterisk param:
HOST = '127.0.0.1'
PORT = 5038
p = '''Action: Login
Events: off
Username: %(username)s
Secret: %(password)s
ActionID: 1

Action: Originate
ActionID: 2
Channel: Local/s@test_leg
Exten: %(phone_to_dial)s
Context: from_user
Variable: test_id=%(test_id)s
priority: 1

Action: Logoff
ActionID: 5

'''

# other param:
# TIME = '%Y-%m-%d %H:%M:%S.%f'
TIME_PREFIX = '%Y-%m-%d %H:%M:%S'
FETCH_LIMIT = 10
LOG_PATH = 'init_call.log'
SLEEP_PAUSE = 30  # задержка между отправкой вызов и проверкой результата
SELECT_DELAY = 45  # в рамках данного таймаута будем пытаться найти исх и вх вызов

text = 'New telephony Alarm! Test call failed'
phones = ('+79163311455')


# phones = ('+79163311455', '+79263374993','+79811976054','+79052510079','+79675117465','+79189514440')

# test numbers:
# 9626841525

def time_now(time_prefix):
    return str(datetime.now().strftime(time_prefix))


def send_sms(text, phone, test_number):
    request_id = random.randint(0, 999999999999)
    print('request_id = {}'.format(request_id))

    m = hashlib.md5()
    m.update(str(request_id) + REDSMS_API_KEY)
    secret = m.hexdigest()
    print('secret = {}'.format(secret))

    data = {
        'login': REDSMS_LOGIN,
        'ts': request_id,
        'secret': secret,
        'route': REDSMS_ROUTE,
        'to': phone,
        'text': text + ', ' + test_number,
    }

    headers = {
        'Authorization': "Bearer",
    }

    requests.post(REDSMS_URL, headers=headers, data=data, stream=True)


def click_to_call(phone_to_dial, username, password, local_user):
    pattern = p % {
        'phone_to_dial': phone_to_dial,
        'username': username,
        'password': password,
        'local_user': local_user,
        'test_id': test_id}

    s = socket.socket()
    s.connect((HOST, PORT))

    data = s.recv(1024)
    for l in pattern.split('\n'):
        s.send(l + '\r\n')
        if l == "":
            data = s.recv(1024)
            print data
    data = s.recv(1024)

    s.close()


def insert_test_call_info():
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        sql = "insert into test_call (anum, bnum, time, direction, test_id) values " \
              "('{}', '{}', (select now()), {}, '{}')".format(anum, bnum, 0, test_id)

        logging.info(" sql = {} ".format(sql))
        print(" sql = {} ".format(sql))
        x.execute(sql)
        conn.commit()

    except:
        logging.info("{} | {} | something went wrong | insert test call info ".format(time_now(TIME_PREFIX), test_id))
        print('something went wrong | insert test call info')
        conn.rollback()
        conn.close()


def select_test_call_info():
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        select_request = "select direction from test_call where " \
                         "ROUND(TIME_TO_SEC(timediff(CURRENT_TIMESTAMP, time))) <= {} " \
                         "and bnum like '%{}' " \
                         "and status={}".format(SELECT_DELAY, str(bnum)[5::], 0)

        print("try to find income test call, sql = {} ".format(select_request))
        logging.info("{} | {} | try to find income test call, sql = {} "
                     .format(time_now(TIME_PREFIX), test_id, select_request))

        x.execute(select_request)

        result = x.fetchmany(FETCH_LIMIT)

        print('result = {}'.format(result))
        logging.info("{} | {} | result = {} ".format(time_now(TIME_PREFIX), test_id, result))
        return result

    except:
        logging.info("{} | {} | something went wrong | try to find income test call "
                     .format(time_now(TIME_PREFIX), test_id))
        print('something went wrong | try to find income test call')

        conn.rollback()
        conn.close()
        return None

def change_test_call_status(from_status, to_status):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        sql = "update test_call set status = {} where status = {}".format(to_status, from_status)

        logging.info("{} | {} | change status from {} to {}, sql update: {} "
                     .format(time_now(TIME_PREFIX), test_id, from_status, to_status, sql))
        print("change status from {} to {}, sql update: {} ".format(from_status, to_status, sql))
        x.execute(sql)
        conn.commit()

    except:
        logging.info("{} | {} | something went wrong | update ".format(time_now(TIME_PREFIX), test_id))
        print('something went wrong | update')
        conn.rollback()
        conn.close()

def send_sms_all_subscribers(subscribers):
    # for phone in phones:
    #     send_sms(text, phone, bnum)
    for subscriber in subscribers:
        send_sms(text, subscriber, bnum)



if __name__ == '__main__':
    # print(time_now(TIME))

    anum = sys.argv[1]
    bnum = sys.argv[2]
    test_id = random.randint(0, 999999999999)

    logging.basicConfig(filename=LOG_PATH, level=logging.INFO)
    logging.info("{} | {} | Test start, anum={}, bnum={}".format(time_now(TIME_PREFIX), test_id, anum, bnum))

    insert_test_call_info()

    click_to_call(bnum, username='admin', password='test1234', local_user=anum)
    logging.info("{} | {} | init call to SIP user {}".format(time_now(TIME_PREFIX), test_id, anum))

    print('sleep start')
    logging.info("{} | {} | start sleep pause {}".format(time_now(TIME_PREFIX), test_id, SLEEP_PAUSE))

    time.sleep(SLEEP_PAUSE)

    print('sleep stop')
    logging.info("{} | {} | finish sleep pause".format(time_now(TIME_PREFIX), test_id))

    result = select_test_call_info()

    if result and len(result) >= 2:
        print('test was successfully completed')
        logging.info("{} | {} | test was successfully completed".format(time_now(TIME_PREFIX), test_id))

    else:
        print('Alarm!')
        logging.info("{} | {} | Alarm!".format(time_now(TIME_PREFIX), test_id))
        send_sms_all_subscribers(phones)

    change_test_call_status(0, 1)
    logging.info(" ")