from guest_list import insert_guest


def test_insert_guest_saves_guest(clean_guest_list, first_name,
                                  last_name, guest_list_from_db):
    """Make sure a guest record is stored when insert guest is called"""

    # Call the function being tested
    insert_guest(first_name, last_name)

    # Get the guest list straight from the db and make sure there's only 1
    # item in it
    guest_list = guest_list_from_db()
    assert len(guest_list) == 1

    # Assert the database row is what we inserted
    assert guest_list[0] == (first_name, last_name, None)





