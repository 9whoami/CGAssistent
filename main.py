#!/usr/bin/python3
# -*- coding: utf-8 -*-

from random import choice
from string import ascii_letters, digits
import threading
from cg import CyberGhost

__author__ = 'whoami'
__version__ = '0.1.2'
__date__ = '02.01.16 13:26'
__description__ = """
Helper for regidtration accounts in cyberghostvpn.com
Первым закроется тот драйвер что был первым открыт!
"""

OUTFILE = "users.txt"
FROMFILE = "in.txt"
REGURL = "https://account.cyberghostvpn.com/en_us/create?"
XPATH = dict(
    puk=".//*[@id='loginForm']/div[2]/form/input[3]",
    login=".//*[@id='loginForm']/div[1]/div[2]/form/input[1]",
    passwd=[".//*[@id='loginForm']/div[1]/div[2]/form/input[2]",
            ".//*[@id='loginForm']/div[1]/div[2]/form/input[3]", ],
)


def generation_passwd(length):
    spec = '!@#$%&*?^'
    all_symbols = digits + ascii_letters

    res = []
    for _ in range(length):
        res.append(choice(all_symbols))

    password = ''.join(res)
    return password


def thread(my_func):
    """
    Декоратор для запуска функции в потоке
    :param my_func: functions
    :return: functions
    """

    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=my_func, args=args, kwargs=kwargs)
        my_thread.start()

    return wrapper


@thread
def main():
    cg = CyberGhost(None, XPATH, None, REGURL)
    cg.driver_start()
    login, passwd = generation_passwd(6), generation_passwd(6)
    cg.registration([login, passwd])
    puk = input(login + " press enter to close:\n")
    cg.driver_stop()
    with open(OUTFILE, 'a') as f:
        f.writelines(':'.join((login, passwd, puk,)))
        f.write('\n')


if __name__ in "__main__":
    count = int(input("Type count:"))
    threads_limit = int(input("Count thread:"))
    threads_limit += threading.active_count()
    for i in range(int(count)):
        while threading.active_count() >= threads_limit:
            pass
        main()
