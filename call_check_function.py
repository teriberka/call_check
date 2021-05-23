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


def click_to_call(phone_to_dial, username, password, callerid, test_id, gateway):
    pattern = p % {
        'phone_to_dial': phone_to_dial,
        'username': username,
        'password': password,
        # 'local_user': local_user,
        'test_id': test_id,
        'gsm_gw': gateway,
        'callerid': callerid}

    s = socket.socket()
    s.connect((ast_host, ast_port))

    data = s.recv(1024)
    for l in pattern.split('\n'):
        s.send(l + '\r\n')
        if l == "":
            data = s.recv(1024)
            # print data
    data = s.recv(1024)

    s.close()


def insert_test_call_info(anum, bnum, test_id, gateway):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        sql = "insert into check_call (callerid, phone, time, direction, test_id, gateway) values " \
              "('{}', '{}', (select now()), {}, '{}', '{}')".format(anum, bnum, 0, test_id, gateway)

        print(" sql = {} ".format(sql))
        x.execute(sql)
        conn.commit()

    except:
        print('something went wrong | insert test call info')
        conn.rollback()
        conn.close()


def select_inbound_call(test_id, direction, status):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        select_request = "select status from check_call where test_id={} " \
                         "and direction={} " \
                         "and status={}".format(test_id, direction, status)

        print("select inbound call, sql = {} ".format(select_request))

        x.execute(select_request)
        result = x.fetchone()
        print('result = {}'.format(result))
        return result

    except:
        print('something went wrong | try to select inbound call')

        conn.rollback()
        conn.close()
        return None


def update_call_status(test_id, status):
    conn = MySQLdb.connect(host=db_host, port=db_port, user=db_user, passwd=db_password, db=db_database, charset='utf8')
    x = conn.cursor()

    try:
        sql = "update check_call set status = {} where test_id = {}".format(status, test_id)
        print('change status to {}, where test_id: {}'.format(status, test_id))
        print('sql update: {} '.format(sql))

        x.execute(sql)
        conn.commit()

    except:
        print('something went wrong | try to update call status')
        conn.rollback()
        conn.close()


def write_alarm(phone, callerid, time, gateway, test_id, status):
    with open(ALARM_FILE_NAME, 'a') as text_file:
        text_file.write("{};{};{};{};{};{}\n".format(phone, callerid, time, gateway, test_id, status))
