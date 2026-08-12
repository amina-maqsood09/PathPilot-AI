import json
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY, MODEL_NAME

# Create the Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


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
    from app.prompts import SYSTEM_PROMPT

    user_data = build_user_context()
    full_system_prompt = SYSTEM_PROMPT.format(user_data=user_data)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_question,
        config=types.GenerateContentConfig(
            system_instruction=full_system_prompt
        )
    )

    return response.text
def ask_pathpilot_with_notes(user_question, note_content):
    """Send a question to Gemini along with specific note content and profile/memory context."""
    from app.prompts import SYSTEM_PROMPT

    user_data = build_user_context()
    full_system_prompt = SYSTEM_PROMPT.format(user_data=user_data)

    combined_prompt = f"""Here is study material provided by the user:

---
{note_content}
---

Base your answer primarily on this material. If the material doesn't cover something, say so clearly rather than inventing information.

User's question: {user_question}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=combined_prompt,
        config=types.GenerateContentConfig(
            system_instruction=full_system_prompt
        )
    )

    return response.text
def ask_pathpilot_career(job_description):
    """Compare the user's profile against a job/internship description."""
    from app.prompts import SYSTEM_PROMPT

    user_data = build_user_context()
    full_system_prompt = SYSTEM_PROMPT.format(user_data=user_data)

    career_prompt = f"""Here is a job/internship description:

---
{job_description}
---

Compare this job description against the user's profile (skills, projects, certifications) provided in your context.

Respond in this exact structure:

MATCHES
(List skills/requirements the user's profile already satisfies, with a checkmark)

GAPS
(List skills/requirements missing from the user's profile, with a warning symbol)

PRIORITY
(Rank the top 2-3 gaps that matter most, in order)

NEXT ACTION
(One concrete, actionable next step to close the top-priority gap)

Do not exaggerate the user's qualifications. If a requirement is ambiguous or partially met, say so honestly.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=career_prompt,
        config=types.GenerateContentConfig(
            system_instruction=full_system_prompt
        )
    )

    return response.text
def ask_pathpilot_skillgap(skill_options):
    """Compare multiple skill options and recommend which to prioritize next."""
    from app.prompts import SYSTEM_PROMPT

    user_data = build_user_context()
    full_system_prompt = SYSTEM_PROMPT.format(user_data=user_data)

    options_text = ", ".join(skill_options)

    skillgap_prompt = f"""The user is deciding what to learn next and is considering these options: {options_text}

Using the user's profile (career goal, target roles, current skills, projects) and memory (weak topics, learning progress), compare these options and recommend ONE as the highest priority.

Respond in this exact structure:

RECOMMENDED SKILL
(The single skill you recommend learning next)

REASON
(Explain why this beats the other option(s), grounded in the user's actual profile/goals/gaps — do not invent evidence)

SUGGESTED LEARNING ACTION
(One concrete first step to start learning it)

OPTIONAL MINI-PROJECT
(A small practice project idea to apply this skill)

Be direct and avoid a long generic roadmap — this should be a clear, prioritized recommendation.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=skillgap_prompt,
        config=types.GenerateContentConfig(
            system_instruction=full_system_prompt
        )
    )

    return response.text