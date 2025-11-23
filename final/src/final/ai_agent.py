import os
from typing import List, Dict

from openai import OpenAI

MODEL = "gpt-4.1-mini"

# Create a client instance using the environment variable (may be None)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _ensure_api_key() -> None:
    """Raise a clear error if the API key is missing.

    The `client` is constructed at import time using the environment
    variable, but we still validate at call time to provide a helpful
    RuntimeError when the key is not set.
    """
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set. Please set it to your OpenAI API key."
        )


def _call_chat(messages: List[Dict], model: str = MODEL, temperature: float = 0.3, max_tokens: int = 300) -> str:
    """Call the OpenAI Chat Completions API via the new client and return text.

    Uses `client.chat.completions.create(...)` and returns the assistant
    content string. Raises RuntimeError when API key is missing or an API
    error occurs.
    """
    _ensure_api_key()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")


def summarize_description(description: str) -> str:
    """Return a very short (5-10 words) task title for the given description.

    The function sends the description to the Chat Completions API and returns
    the single-line title produced by the model. If the API key is missing a
    RuntimeError will be raised.
    """
    system = "You are an assistant that writes very short task titles (5–10 words)."
    user = (
        "Write a single short title for this task description. "
        "Do NOT include any explanation or extra text.\n\n"
        f"Description:\n{description}"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    return _call_chat(messages, temperature=0.2, max_tokens=60)


def generate_plan(tasks: List[Dict]) -> str:
    """Generate an ordered plan for what to do today from a list of tasks.

    The function builds a concise text representation of the open tasks
    (including `id`, `title`, `priority`, and `due_date`) and asks the model
    to produce a numbered plan. It returns the model's response as plain text.

    Args:
        tasks: list of task dictionaries (typically from state["tasks"]).

    Returns:
        str: the model's plain-text response.
    """
    # Filter out tasks that are marked completed/done/closed
    open_tasks = []
    for t in tasks:
        if t is None:
            continue
        status = str(t.get("status", "")).lower()
        completed_flag = bool(t.get("completed") or t.get("done"))
        if completed_flag or status in ("done", "completed", "closed"):
            continue
        open_tasks.append(t)

    if not open_tasks:
        tasks_text = "No open tasks."
    else:
        lines = []
        for t in open_tasks:
            tid = t.get("id", "")
            title = str(t.get("title", t.get("description", ""))).replace("\n", " ")
            priority = t.get("priority", "")
            due = t.get("due_date", t.get("due", ""))
            lines.append(f"ID: {tid} | Title: {title} | Priority: {priority} | Due: {due}")
        tasks_text = "\n".join(lines)

    system = (
        "You are an assistant that, given a list of tasks, produces a concise "
        "ordered plan for what to do today."
    )
    user = (
        "Given this list of tasks, produce an ordered plan for what to do today. "
        "Output as a numbered list and be concise. Do not add extra commentary.\n\n"
        f"Tasks:\n{tasks_text}"
    )
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    return _call_chat(messages, temperature=0.4, max_tokens=500)


__all__ = ["summarize_description", "generate_plan"]
