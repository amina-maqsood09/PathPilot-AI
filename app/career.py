import os

CAREER_DIR = "data/career"


def list_job_descriptions():
    """Return a list of available job/internship description files."""
    if not os.path.exists(CAREER_DIR):
        return []
    return [f for f in os.listdir(CAREER_DIR) if f.endswith((".txt", ".md"))]


def load_job_description(filename):
    """Load the content of a specific job description file."""
    path = os.path.join(CAREER_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()