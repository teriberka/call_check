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

LOG_PATH = 'call_check.log'
ALARM_FILE_NAME = 'call_check.alarm'

SLEEP_PAUSE = 15  # задержка между отправкой вызов и проверкой результата
DELAY = 2  # пауза между тестами

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

gateways = (('gsm1', 9831309165),
            ('gsm2', 89232536164),
            ('gsm3', 89628346810),
            ('gsm4', 9538895175))

