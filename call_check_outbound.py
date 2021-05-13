#!/usr/bin/python
# coding=utf-8

import time
import logging

from call_check_config import *
from call_check_function import *


if __name__ == '__main__':
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

    for phone in phones:
        test_id = random.randint(0, 999999999999)
        logging.info("{} | {} | Test start, anum={}, bnum={}".format(time_now(TIME_PREFIX), test_id, callerid, phone))

        insert_test_call_info(callerid, phone, test_id)

        logging.info("{} | {} | init call to SIP user {}".format(time_now(TIME_PREFIX), test_id, phone))
        click_to_call(phone, username=ast_username, password=ast_userpass, local_user=callerid, test_id)

        print('sleep start')
        logging.info("{} | {} | start sleep pause {}".format(time_now(TIME_PREFIX), test_id, SLEEP_PAUSE))

        time.sleep(SLEEP_PAUSE)

        print('sleep stop')
        logging.info("{} | {} | finish sleep pause".format(time_now(TIME_PREFIX), test_id))

        result = select_test_call_info(phone)

        if result and len(result) >= 2:
            print('test was successfully completed')
            logging.info("{} | {} | test was successfully completed".format(time_now(TIME_PREFIX), test_id))

        else:
            print('Alarm!')
            logging.info("{} | {} | Alarm!".format(time_now(TIME_PREFIX), test_id))
            # send_sms_all_subscribers()

    change_test_call_status(0, 1)
