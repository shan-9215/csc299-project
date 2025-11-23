from final.storage import next_note_id


def test_next_note_id_empty():
    state = {"notes": [], "tasks": []}
    assert next_note_id(state) == 1


def test_next_note_id_nonempty():
    state = {"notes": [{"id": 1}, {"id": 3}], "tasks": []}
    assert next_note_id(state) == 4


def test_list_notes_no_crash():
    from final import commands

    # Should not raise
    commands.list_notes({"notes": []})
    commands.list_notes({"notes": [{"id": 1, "title": "A", "tags": ["x"]}]})
