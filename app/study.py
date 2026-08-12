import os

NOTES_DIR = "data/notes"


def list_notes():
    """Return a list of available note filenames."""
    if not os.path.exists(NOTES_DIR):
        return []
    return [f for f in os.listdir(NOTES_DIR) if f.endswith((".txt", ".md"))]


def load_note(filename):
    """Load the content of a specific note file."""
    path = os.path.join(NOTES_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()