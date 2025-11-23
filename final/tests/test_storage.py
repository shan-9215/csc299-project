from final.storage import load_state


def test_load_state_initial():
    state = load_state()
    assert isinstance(state, dict)
    assert "tasks" in state and "notes" in state
    assert isinstance(state["tasks"], list)
    assert isinstance(state["notes"], list)
