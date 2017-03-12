import sqlite3


conn = sqlite3.connect('guest_list.db')
cursor = conn.cursor()


def insert_guest(first_name, last_name):
    query = """INSERT INTO guests
                   VALUES (null, ?, ?, null)"""

    with conn:
        result = cursor.execute(query, (first_name,
                                        last_name,))
        return result.lastrowid


def delete_guest(first_name, last_name):
    query = "DELETE FROM guests WHERE firstName=? and lastName=?"
    with conn:
        result = cursor.execute(query, (first_name, last_name,))
        if result.rowcount == 0:
            raise ValueError("Guest not found")


def get_guest(first_name, last_name):
    query = "SELECT * FROM guests WHERE firstName=? AND lastName=?"
    with conn:
        result = cursor.execute(query, (first_name, last_name,))
        try:
            return next(result)
        except StopIteration:
            raise ValueError


def get_guest_list():
    query = 'SELECT * FROM guests'
    with conn:
        return list(cursor.execute(query))


def rsvp(first_name, last_name, answer):
    answer = 1 if answer else 0
    query = "UPDATE guests SET rsvp=? WHERE firstName=? AND lastName=?"
    with conn:
        result = cursor.execute(query, (answer, first_name, last_name))
        if result.rowcount == 0:
            raise ValueError("Guest not found")
