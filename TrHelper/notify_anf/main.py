import time
import argparse
from notify_anf import ANFNotify


def loop(sleep=60*2):
    '''Main loop. Check for new articles in ANFnews' website by
    comparison of titles with particular frequency. In case
    of new article the link will be printed in command line.'''

    print('Monitoring ANF website')
    check = ANFNotify()
    check.get_info()
    check.notify()
    count = 0
    while 1:
        try:
            a = ANFNotify()
            f_check, *l = a.get_info()
            time.sleep(sleep)
            sec_sheck, link = a.get_info()

            if f_check != sec_sheck:
                a.notify()
                count += 1
                print('\n\t{}. {}'.format(count, link))
                
        except (KeyboardInterrupt, TypeError):
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
