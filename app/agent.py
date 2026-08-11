import json
import google.generativeai as genai
from app.config import GEMINI_API_KEY, MODEL_NAME
from app.prompts import SYSTEM_PROMPT

# Configure Gemini with our API key
genai.configure(api_key=GEMINI_API_KEY)


def load_json(file_path):
    """Load a JSON file and return its contents."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_user_context():
    """Combine profile.json and memory.json into one context string."""
    profile = load_json("data/profile.json")
    memory = load_json("data/memory.json")

    combined = {
        "profile": profile,
        "memory": memory
    }

    return json.dumps(combined, indent=2)


def ask_pathpilot(user_question):
    """Send the user's question to Gemini along with their personal context."""
    user_data = build_user_context()

    full_prompt = SYSTEM_PROMPT.format(user_data=user_data)

    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=full_prompt
    )

    response = model.generate_content(user_question)

    return response.text