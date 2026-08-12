import json
from datetime import date

MEMORY_FILE = "data/memory.json"


def load_memory():
    """Load memory.json contents."""
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory_data):
    """Save updated data back into memory.json."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=2)


def record_mistake(topic, concept):
    """Log a mistake. If the concept already exists, update it instead of duplicating."""
    memory = load_memory()

    for item in memory["mistakes"]:
        if item["topic"].lower() == topic.lower() and item["concept"].lower() == concept.lower():
            item["attempts"] += 1
            item["last_reviewed"] = str(date.today())
            item["status"] = "needs_revision"
            save_memory(memory)
            return f"Updated: {topic} - {concept} (attempt #{item['attempts']})"

    # New mistake entry
    new_entry = {
        "topic": topic,
        "concept": concept,
        "attempts": 1,
        "correct": 0,
        "last_reviewed": str(date.today()),
        "status": "needs_revision"
    }
    memory["mistakes"].append(new_entry)
    save_memory(memory)
    return f"Recorded new weak topic: {topic} - {concept}"


def mark_as_improved(topic, concept):
    """Mark a concept as reviewed/improved (correct answer)."""
    memory = load_memory()

    for item in memory["mistakes"]:
        if item["topic"].lower() == topic.lower() and item["concept"].lower() == concept.lower():
            item["correct"] += 1
            item["last_reviewed"] = str(date.today())
            if item["correct"] >= item["attempts"]:
                item["status"] = "improved"
            save_memory(memory)
            return f"Marked as improved: {topic} - {concept}"

    return f"No record found for {topic} - {concept}"


def get_weak_topics():
    """Return all topics still marked as needing revision."""
    memory = load_memory()
    return [item for item in memory["mistakes"] if item["status"] == "needs_revision"]