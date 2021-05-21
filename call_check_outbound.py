#!/usr/bin/python
# coding=utf-8

import time
import logging

from call_check_config import *
from call_check_function import *


if __name__ == '__main__':
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO)
    print('test start!')
    logging.info("{} | {} | test start!".format(time_now(TIME_PREFIX), 'None'))

    for gateway in gateways:
        print('use for test gateway: {}, sim callerid: {}'.format(gateway[0], gateway[1]))
        logging.info("{} | {} | use for test gateway: {}, sim callerid: {}".
                     format(time_now(TIME_PREFIX), 'None', gateway[0], gateway[1]))

        for phone in phones:
            test_id = random.randint(0, 999999999999)

            print('test phone: {}'.format(phone))
            logging.info("{} | {} | test phone: {}".format(time_now(TIME_PREFIX), test_id, phone))

            print('insert test call info')
            logging.info("{} | {} | insert test call info".format(time_now(TIME_PREFIX), test_id))
            insert_test_call_info(gateway[1], phone, test_id, gateway[0])

            print('start outbound call')
            logging.info("{} | {} | start outbound call".format(time_now(TIME_PREFIX), test_id))
            click_to_call(phone, username=ast_username, password=ast_userpass, callerid=gateway[1],
                          test_id=test_id, gateway=gateway[0])

            print('sleep pause {} seconds (we wait inbound call)'.format(SLEEP_PAUSE))
            logging.info("{} | {} | sleep pause {} seconds (we wait inbound call)".
                         format(time_now(TIME_PREFIX), test_id, SLEEP_PAUSE))
            time.sleep(SLEEP_PAUSE)


            print('check result')
            logging.info("{} | {} | check result".format(time_now(TIME_PREFIX), test_id))
            result = select_inbound_call(test_id, 1, 1)

            try:
                if result[0] == 1:
                    print('Ok! test was successfully completed')
                    logging.info("{} | {} | Ok! test was successfully completed".format(time_now(TIME_PREFIX), test_id))
                    update_call_status(test_id, 5)
                else:
                    print('Alarm! test failed')
                    logging.info("{} | {} | Alarm! test failed".format(time_now(TIME_PREFIX), test_id))
                    update_call_status(test_id, 2)

                    write_alarm(phone, gateway[1], time_now(TIME_PREFIX), gateway[0], test_id, '2')

            except TypeError:
                print('Alarm! test failed')
                logging.info("{} | {} | Alarm! test failed".format(time_now(TIME_PREFIX), test_id))
                update_call_status(test_id, 2)

                write_alarm(phone, gateway[1], time_now(TIME_PREFIX), gateway[0], test_id, '2')

            print('pause {} seconds between tests'.format(DELAY))
            logging.info("{} | {} | pause {} seconds between tests".
                         format(time_now(TIME_PREFIX), test_id, DELAY))
            print('')
            time.sleep(DELAY)

    print('test end!')
    logging.info("{} | {} | test end!".format(time_now(TIME_PREFIX), 'None'))
