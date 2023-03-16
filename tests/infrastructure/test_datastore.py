import pytest
from hamcrest import assert_that, empty, equal_to

from src.intrastructure import datastore
from src.intrastructure.datastore import DatastoreError


class TestFetchOneByField:
    def test_raises_when_entry_type_not_found(self):
        with pytest.raises(DatastoreError, match="No entry type 'users' found"):
            datastore.fetch_one_by_field("users", "id", "1")

    def test_raise_when_no_match_is_found(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        with pytest.raises(
            DatastoreError, match="No entry found in 'users' for id='2'"
        ):
            datastore.fetch_one_by_field("users", "id", "2")

    def test_returns_the_entry(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        entry = datastore.fetch_one_by_field("users", "id", "1")
        assert_that(
            entry, equal_to(dict(id="1", name="Kevin", favourite_colour="yellow"))
        )

    def test_raises_when_multiple_entries_found(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        datastore.save("users", dict(id="2", name="Norbert", favourite_colour="yellow"))
        with pytest.raises(
            DatastoreError,
            match="Expected 1 entry in 'users' for favourite_colour='yellow' "
            "but found 2",
        ):
            datastore.fetch_one_by_field("users", "favourite_colour", "yellow")

    def test_returns_the_entry_for_the_correct_type(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        datastore.save(
            "admins", dict(id="1", name="Felonius Gru", favourite_colour="black")
        )
        entry = datastore.fetch_one_by_field("users", "id", "1")
        assert_that(
            entry, equal_to(dict(id="1", name="Kevin", favourite_colour="yellow"))
        )


class TestFetchByField:
    def test_raises_when_entry_type_not_found(self):
        with pytest.raises(DatastoreError, match="No entry type 'users' found"):
            datastore.fetch_by_field("users", "favourite_colour", "yellow")

    def test_returns_empty_list_when_no_entries_found(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        entries = datastore.fetch_by_field("users", "favourite_colour", "red")
        assert_that(entries, empty())

    def test_returns_matching_entries(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        datastore.save("users", dict(id="2", name="Norbert", favourite_colour="yellow"))
        datastore.save(
            "users", dict(id="2", name="Agnes Gru", favourite_colour="orange")
        )
        datastore.save(
            "admins", dict(id="1", name="Felonius Gru", favourite_colour="black")
        )
        entries = datastore.fetch_by_field("users", "favourite_colour", "yellow")
        assert_that(
            entries,
            equal_to(
                [
                    dict(id="1", name="Kevin", favourite_colour="yellow"),
                    dict(id="2", name="Norbert", favourite_colour="yellow"),
                ]
            ),
        )


class TestUpdate:
    def test_raises_when_entry_type_not_found(self):
        with pytest.raises(DatastoreError, match="No entry type 'users' found"):
            datastore.update("users", "id", dict(id=1, name="Bob"))

    def test_raises_when_no_matching_entries_are_found(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        datastore.save("users", dict(id="2", name="Kevin", favourite_colour="yellow"))
        with pytest.raises(
            DatastoreError,
            match="Expected 1 entry in 'users' for id='7' but found none",
        ):
            datastore.update(
                "users",
                "id",
                dict(id="7", name="Kevin", favourite_colour="still yellow"),
            )

    def test_raises_when_multiple_entries_match(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        datastore.save("users", dict(id="2", name="Kevin", favourite_colour="yellow"))
        with pytest.raises(
            DatastoreError,
            match="Expected 1 entry in 'users' for name='Kevin' but found 2",
        ):
            datastore.update(
                "users",
                "name",
                dict(id="1", name="Kevin", favourite_colour="still yellow"),
            )

    def test_updates_the_entry(self):
        datastore.save("users", dict(id="1", name="Kevin", favourite_colour="yellow"))
        datastore.update(
            "users", "id", dict(id="1", name="Kevin", favourite_colour="still yellow")
        )
        entry = datastore.fetch_one_by_field("users", "id", "1")
        assert_that(
            entry, equal_to(dict(id="1", name="Kevin", favourite_colour="still yellow"))
        )
