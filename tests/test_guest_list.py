from guest_list import insert_guest, delete_guest, get_guest, get_guest_list
import pytest


def test_insert_guest_saves_guest(clean_guest_list, first_name,
                                  last_name, guest_list_from_db,
                                  expected_db_row):

    # Call the function being tested
    insert_guest(first_name, last_name)

    # Get the guest list straight from the db and make sure there's only 1
    # item in it
    guest_list = guest_list_from_db()
    assert len(guest_list) == 1

    # Assert the database row is what we inserted
    assert guest_list[0] == expected_db_row


def test_delete_guest_raises(clean_guest_list, first_name, last_name):
    # There hasn't been data pre-populated, so this should throw and error
    with pytest.raises(ValueError):
        delete_guest(first_name, last_name)


def test_delete_guest_deletes(clean_guest_list, insert_one_guest,
                              guest_list_from_db, first_name, last_name,
                              expected_db_row):
    # Insert a guest
    insert_one_guest()

    # Assert there is a guest
    guest_list = guest_list_from_db()
    assert len(guest_list) == 1
    assert guest_list[0] == expected_db_row

    # call delete_guest
    delete_guest(first_name, last_name)

    # assert there are no guests in the db
    guest_list = guest_list_from_db()
    assert len(guest_list) == 0


def test_get_guest_raises_if_not_found(clean_guest_list, first_name, last_name):
    with pytest.raises(ValueError):
        get_guest(first_name, last_name)


def test_get_guest_finds_existing_guest(clean_guest_list, first_name,
                                        last_name, insert_one_guest,
                                        guest_list_from_db, expected_db_row):
    # Insert a guest so there is one to find
    insert_one_guest()
    assert len(guest_list_from_db()) == 1

    # Call the function and assert the return value is the guest inserted
    result = get_guest(first_name, last_name)
    assert result == expected_db_row


def test_get_guest_list_returns_empty_list_if_no_guests(clean_guest_list):
    result = get_guest_list()
    assert result == []


def test_get_guest_list_returns_guest_list(clean_guest_list, insert_one_guest,
                                           expected_db_row):
    # Insert a couple guests (the same guest twice..)
    insert_one_guest()
    insert_one_guest()

    # Assert the guest list has two guests and they're both the same
    guest_list = get_guest_list()
    assert len(guest_list) == 2
    assert all(guest == expected_db_row for guest in guest_list)

