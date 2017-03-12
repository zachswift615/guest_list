import pytest
import sqlite3


@pytest.fixture
def first_name():
    return 'Rick'


@pytest.fixture
def last_name():
    return 'Grimes'


@pytest.fixture
def database_id():
    return 1


@pytest.fixture
def expected_db_row(database_id, first_name, last_name):
    return database_id, first_name, last_name, None


@pytest.fixture()
def conn():
    return sqlite3.connect('guest_list.db')


@pytest.fixture
def cursor(conn):
    return conn.cursor()


@pytest.fixture
def guest_list_from_db(conn, cursor):
    def inner():
        with conn:
            return list(cursor.execute("SELECT * FROM guests"))
    return inner # So that it can be called multiple times


@pytest.fixture
def clean_guest_list(conn, cursor):
    # define nested function to drop table
    def drop_table():
        with conn:
            cursor.execute("DROP TABLE IF EXISTS guests")

    # drop the table before creating a new one
    drop_table()

    # create a new table
    TABLEDEF = '''CREATE TABLE IF NOT EXISTS guests(
                          id INTEGER PRIMARY KEY, firstName TEXT,
                          lastName TEXT, RSVP INTEGER)'''
    with conn:
        cursor.execute(TABLEDEF)

    yield # <-- The fixture pauses here lets the test run

    # drop the table after the test is finished
    drop_table()


@pytest.fixture
def insert_one_guest(first_name, last_name, conn, cursor):
    def inner():
        with conn:
            cursor.execute('''INSERT INTO guests VALUES
                           (null, ?, ?, null)''', (first_name, last_name,))
    return inner


@pytest.fixture(params=[True, False])
def rsvp_status(request):
    return request.param

