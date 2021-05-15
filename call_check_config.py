#!/usr/bin/python
# coding=utf-8


# mysql connect param:
db_host = '127.0.0.1'
db_port = 3306
db_user = "admin"
db_password = "c@ll!ch3ck"
db_database = "asterisk"

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
Variable: test_id=%(test_id)s,callerid=%(callerid)s,gsm_gw=%(gsm_gw)s
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

phones = ('84996660209',
          '83832888809',
          '83432888809',
          '88432707009',
          '88462888809',
          '88622606009',
          '84712666609',
          '83842222209',
          '83843222209',
          '88332666609',
          '84712666609',
          '84112666609')

gateways = ('gsm1',
            'gsm2',
            'gsm3',
            'gsm4')

callerid = '79163311455'
