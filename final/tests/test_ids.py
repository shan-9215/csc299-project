from final.storage import next_task_id, next_note_id


def test_next_task_id_empty():
    state = {"tasks": [], "notes": []}
    assert next_task_id(state) == 1


def test_next_task_id_nonempty():
    state = {"tasks": [{"id": 1}, {"id": 4}], "notes": []}
    assert next_task_id(state) == 5
