import time
import argparse
import pyperclip
from notify_anf import ANFNotify


def loop(sleep=10):
    '''Main loop. Check for new articles in ANFnews' website by
    comparison of titles with particular frequency. In case
    of new article the link will be printed in command line.'''

    print('Monitoring ANF website')
    a = ANFNotify()
    f_check, *rest = a.get_info()
    a.notify()
    count = 0
    while 1:
        try:
            #time.sleep(sleep)
            b = ANFNotify()
            sec_sheck, link, symbol_number = b.get_info()

            if f_check != sec_sheck:
                b.notify()
                pyperclip.copy(link)
                count += 1
                print(
                    '\n\t{}. {}\n\tInfo: {} symbols in article'.format(
                    count, link, symbol_number
                    )
                    )
                a = b
                f_check, *rest = a.get_info()

        except KeyboardInterrupt:
            print('\nStop monitoring of ANF')
            break


def argparser():
    '''Allow to change the frequency of checking by writing args in
    command line when programm is started. '''

    parser = argparse.ArgumentParser(
        description='''
        This is the handler to help translators
        to organize the work and get notifications about new articles
        in ANFnews' website'''
        )
    parser.add_argument(
        '-f', '--freq',
        help='establish the frequency in sec of checking website, default=120 sec',
        type=int)
    args = parser.parse_args()
    return args.freq


if __name__ == "__main__":
    sleep = argparser()
    loop(sleep) if sleep else loop()
