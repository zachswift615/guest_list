import pytest
import sqlite3


@pytest.fixture
def first_name():
    return 'Rick'


@pytest.fixture
def last_name():
    return 'Grimes'


@pytest.fixture
def conn():
    return sqlite3.connect('rsvp.db')


@pytest.fixture
def cursor(conn):
    return conn.cursor()


@pytest.fixture
def guest_list_from_db(conn, cursor):
    def inner():
        with conn:
            return list(cursor.execute("SELECT * FROM guests"))
    return inner


@pytest.fixture
def clean_guest_list(conn, cursor):

    def clean():
        with conn:
            cursor.execute("DROP TABLE IF EXISTS guests")

    clean()
    with conn:
        TABLEDEF = '''CREATE TABLE if NOT EXISTS guests
                      (firstName text, lastName text, RSVP integer)'''
        cursor.execute(TABLEDEF)

    yield
    clean()
