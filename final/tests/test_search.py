from final.commands import search_all


def test_search_runs():
    state = {
        "tasks": [
            {"id": 1, "title": "Write essay", "description": "Finish CSC paper", "tags": []}
        ],
        "notes": [
            {"id": 1, "title": "Lecture notes", "content": "AI and PKMS discussion", "tags": []}
        ],
    }

    # Should run without raising
    search_all(state, "essay")
