import sqlite3
from bd_wrapper import bd_conn_wrapper
import datetime

name = 'PeriodsChekingDB'

@bd_conn_wrapper(name)
def setup():
    create = '''\
        CREATE TABLE IF NOT EXIST user (
            id_user integer primary key autoincrement,
            user_name text
        );

        CREATE TABLE IF NOT EXIST data (
            id_data integer primary key autoincrement,
            day text,
            id_user integer
        );
        '''
    c.executescript(create)




@bd_conn_wrapper(name)
def write_to_db():
    write = '''insert into data (day, id_user) values (?, ?)'''
    id_user = c.execute(
        '''select from user id_user where user_name=(?)''',
        chat_id
        )
    args = date.today(), id_user
    c.execute(write, args)


def get_period():
    pass


def get_next_date():
    pass


def add_user_to_bd(chat_id):
    write = '''insert into user (user_name,) values (?,)'''
    c.execute(write, chat_id)


def check_user_in_bd(chat_id):
    select_id = '''select from user id_user where user_name=(?)'''
    id_user = c.execute(select_id, chat_id)
        if not id_user:
            return False
        else:
            return True



def add_dates():
    pass


def show_data():
    pass
