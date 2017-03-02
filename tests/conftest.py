import pytest
import sqlite3


@pytest.fixture
def first_name():
    return 'Rick'


@pytest.fixture
def last_name():
    return 'Grimes'


@pytest.fixture
def expected_db_row(first_name, last_name):
    return first_name, last_name, None


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


@pytest.fixture
def insert_one_guest(first_name, last_name, conn, cursor):
    def inner():
        with conn:
            cursor.execute('''INSERT INTO guests VALUES
                           (?, ?, null)''', (first_name, last_name,))
    return inner
