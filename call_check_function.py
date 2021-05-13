#!/usr/bin/python
# coding=utf-8


import socket
import random
import hashlib
import MySQLdb
import requests

from datetime import datetime
from call_check_config import *


def time_now(time_prefix):
    return str(datetime.now().strftime(time_prefix))


def click_to_call(phone_to_dial, username, password, local_user, test_id):
    pattern = p % {
        'phone_to_dial': phone_to_dial,
        'username': username,
        'password': password,
        'local_user': local_user,
        'test_id': test_id,
        'callerid': callerid}

    s = socket.socket()
    s.connect((ast_host, ast_port))

    data = s.recv(1024)
    for l in pattern.split('\n'):
        s.send(l + '\r\n')
        if l == "":
            data = s.recv(1024)
            print data
    data = s.recv(1024)

    s.close()


def insert_test_call_info(anum, bnum, test_id):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        sql = "insert into check_call (callerid, phone, time, direction, test_id) values " \
              "('{}', '{}', (select now()), {}, '{}')".format(anum, bnum, 0, test_id)

        print(" sql = {} ".format(sql))
        x.execute(sql)
        conn.commit()

    except:
        print('something went wrong | insert test call info')
        conn.rollback()
        conn.close()


def select_test_call_info(bnum):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        select_request = "select direction from check_call where " \
                         "ROUND(TIME_TO_SEC(timediff(CURRENT_TIMESTAMP, time))) <= {} " \
                         "and phone like '%{}' " \
                         "and status={}".format(SELECT_DELAY, str(bnum)[5::], 0)

        print("try to find income test call, sql = {} ".format(select_request))

        x.execute(select_request)
        result = x.fetchmany(FETCH_LIMIT)
        print('result = {}'.format(result))
        return result

    except:
        print('something went wrong | try to find income test call')

        conn.rollback()
        conn.close()
        return None


def change_test_call_status(from_status, to_status):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        sql = "update test_call set status = {} where status = {}".format(to_status, from_status)
        print("change status from {} to {}, sql update: {} ".format(from_status, to_status, sql))
        x.execute(sql)
        conn.commit()

    except:
        print('something went wrong | update')
        conn.rollback()
        conn.close()


