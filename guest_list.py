import sqlite3


conn = sqlite3.connect('rsvp.db')
cursor = conn.cursor()
TABLEDEF = '''CREATE TABLE if not exists guests
              (firstName text, lastName text, RSVP integer)'''
with conn:
    cursor.execute(TABLEDEF)


def insert_guest(first_name, last_name):
    query = "insert into guests values (?, ?, null)"

    with conn:
        cursor.execute(query, (first_name, last_name,))


def delete_guest(first_name, last_name):
    query = "delete from guests where firstName=? and lastName=?"
    with conn:
        result = cursor.execute(query, (first_name, last_name,))
        if result.rowcount == 0:
            raise ValueError("Guest not found")


def get_guest(first_name, last_name):
    query = "select * from guests where firstName=? and lastName=?"
    with conn:
        result = cursor.execute(query, (first_name, last_name,))
        try:
            return next(result)
        except StopIteration:
            raise ValueError


def get_guest_list():
    query = 'select * from guests'
    with conn:
        return list(cursor.execute(query))


def rsvp(first_name, last_name, answer):
    answer = 1 if answer else 0
    query = "update guests set rsvp=? where firstName=? and lastName=?"
    with conn:
        result = cursor.execute(query, (answer, first_name, last_name))
        if result.rowcount == 0:
            raise ValueError("Guest not found")
