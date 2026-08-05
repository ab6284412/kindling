"""Read/write the learner's state.json. Atomic write, corrupt-file fallback."""
from __future__ import annotations

import json
import os
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_PATH = os.path.join(ROOT, "state.json")


def default_state() -> dict:
    return {"stages": {}, "drills": {}, "reads": {}, "notes": {}}


def load() -> dict:
    if not os.path.exists(STATE_PATH):
        return default_state()
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return default_state()
    if not isinstance(data, dict):
        return default_state()
    state = default_state()
    for key in state:
        if isinstance(data.get(key), dict):
            state[key] = data[key]
    # Normalize legacy string-valued notes to the list shape the UI expects.
    for path, note in list(state["notes"].items()):
        if not isinstance(note, list):
            state["notes"][path] = [str(note)]
    return state


def save(state: dict) -> None:
    fd, tmp = tempfile.mkstemp(dir=ROOT, prefix=".state-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, sort_keys=True)
        os.replace(tmp, STATE_PATH)
    except BaseException:
        os.unlink(tmp)
        raise


KINDS = {"stage": "stages", "drill": "drills", "read": "reads"}


def toggle(state: dict, kind: str, path: str) -> bool:
    key = KINDS[kind]
    now = bool(state[key].get(path))
    state[key][path] = not now
    return state[key][path]


def set_note(state: dict, path: str, text: str) -> None:
    if text.strip():
        state["notes"][path] = [text.strip()]
    else:
        state["notes"].pop(path, None)
