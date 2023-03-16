from collections import defaultdict
from typing import Any, Dict, List


class DatastoreError(Exception):
    pass


_ENTRIES: Dict[str, List[Dict[str, Any]]] = defaultdict(list)


Entry = Dict[str, Any]


def clear():
    _ENTRIES.clear()


def save(entry_type: str, entry: Entry) -> None:
    return _ENTRIES[entry_type].append(entry)


def fetch_one_by_field(entry_type: str, field: str, match: Any) -> Entry:
    if entry_type not in _ENTRIES:
        raise DatastoreError(f"No entry type '{entry_type}' found")

    matches = [
        entry
        for entry in _ENTRIES[entry_type]
        if field in entry and entry[field] == match
    ]

    if len(matches) == 0:
        raise DatastoreError(f"No entry found in '{entry_type}' for {field}='{match}'")

    if len(matches) > 1:
        raise DatastoreError(
            f"Expected 1 entry in '{entry_type}' for {field}='{match}' "
            f"but found {len(matches)}"
        )

    return matches[0]


def update(entry_type: str, field: str, entry: Entry) -> None:
    if entry_type not in _ENTRIES:
        raise DatastoreError(f"No entry type '{entry_type}' found")

    indexes = [
        i
        for i, existing_entry in enumerate(_ENTRIES[entry_type])
        if field in existing_entry and existing_entry[field] == entry[field]
    ]

    if len(indexes) == 0:
        raise DatastoreError(
            f"Expected 1 entry in '{entry_type}' for {field}='{entry[field]}' "
            f"but found none"
        )

    if len(indexes) > 1:
        raise DatastoreError(
            f"Expected 1 entry in '{entry_type}' for {field}='{entry[field]}' "
            f"but found {len(indexes)}"
        )

    _ENTRIES[entry_type][indexes[0]] = entry


def fetch_by_field(entry_type: str, field: str, match: Any) -> List[Entry]:
    if entry_type not in _ENTRIES:
        raise DatastoreError(f"No entry type '{entry_type}' found")

    return [
        entry
        for entry in _ENTRIES[entry_type]
        if field in entry and entry[field] == match
    ]
