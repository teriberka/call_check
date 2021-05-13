#!/usr/bin/python
# coding=utf-8


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
ast_username = 'checker'
ast_userpass = 'c@ll!ch3ck'
ast_host = '127.0.0.1'
ast_port = 5038
p = '''Action: Login
Events: off
Username: %(username)s
Secret: %(password)s
ActionID: 1

Action: Originate
ActionID: 2
Channel: Local/s@local
Exten: %(phone_to_dial)s
Context: outbound
Variable: test_id=%(test_id)s,callerid=%(callerid)s
priority: 1

Action: Logoff
ActionID: 5

'''

# other param:
TIME_PREFIX = '%Y-%m-%d %H:%M:%S'
FETCH_LIMIT = 10
LOG_PATH = 'call_check.log'
SLEEP_PAUSE = 30  # задержка между отправкой вызов и проверкой результата
SELECT_DELAY = 45  # в рамках данного таймаута будем пытаться найти исх и вх вызов

text = 'New telephony Alarm! Test call failed'

phones = ('74996660209',
          '73832888809',
          '73432888809',
          '78432707009',
          '78462888809',
          '78622606009',
          '74712666609',
          '73842222209',
          '73843222209',
          '78332666609',
          '74712666609',
          '74112666609')

callerid = '79163311455'
