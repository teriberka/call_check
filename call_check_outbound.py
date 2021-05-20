#!/usr/bin/python
# coding=utf-8

import time
import logging

from call_check_config import *
from call_check_function import *


if __name__ == '__main__':
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO)

    print('test start!')
    for gateway in gateways:
        for phone in phones:
            test_id = random.randint(0, 999999999999)
            # logging.info("{} | {} | Test start, anum={}, bnum={}".format(time_now(TIME_PREFIX), test_id, callerid, phone))

            insert_test_call_info(callerid, phone, test_id, gateway)
            click_to_call(phone, username=ast_username, password=ast_userpass, local_user=callerid, test_id=test_id, gateway=gateway)

            print('sleep start')

            time.sleep(SLEEP_PAUSE)

            print('sleep stop')

            result = select_inbound_call(test_id, 1, 1)

            if result == 1:
                print('test was successfully completed')
                update_call_status(test_id, 5)
            else:
                print('Alarm!')
                update_call_status(test_id, 2)
                logging.info("{};{};{};{};{}".format(phone, time_now(TIME_PREFIX), gateway, test_id, result))

            time.sleep(DELAY)

    print('test end!')
