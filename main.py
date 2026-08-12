from app.agent import ask_pathpilot, ask_pathpilot_with_notes, ask_pathpilot_career, ask_pathpilot_skillgap
from app.memory import record_mistake, mark_as_improved, get_weak_topics
from app.study import list_notes, load_note
from app.career import list_job_descriptions, load_job_description


def print_help():
    print("\nCommands:")
    print("  Just type your question to ask PathPilot")
    print("  'notes'                          -> list available study notes")
    print("  'study: <filename> | <question>' -> ask a question using a specific note")
    print("  'quiz: <filename>'                -> generate a quiz from a note")
    print("  'jobs'                           -> list available job descriptions")
    print("  'career: <filename>'             -> compare your profile against a job description")
    print("  'skillgap: <skill1> vs <skill2>' -> compare two skills and get a priority recommendation")
    print("  'mistake: <topic> | <concept>'   -> log a mistake")
    print("  'improved: <topic> | <concept>'  -> mark a concept as improved")
    print("  'weak topics'                    -> list current weak topics")
    print("  'exit'                           -> quit\n")


def main():
    print("=" * 50)
    print("  PathPilot AI — Your Study & Career Assistant")
    print("=" * 50)
    print_help()

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("PathPilot: Goodbye! Keep growing 🚀")
            break

        if user_input.lower() == "notes":
            notes = list_notes()
            if not notes:
                print("\nPathPilot: No notes found in data/notes/. Add a .txt or .md file there.\n")
            else:
                print("\nPathPilot: Available notes:")
                for n in notes:
                    print(f"  - {n}")
                print()
            continue

        if user_input.lower() == "jobs":
            jobs = list_job_descriptions()
            if not jobs:
                print("\nPathPilot: No job descriptions found in data/career/. Add a .txt file there.\n")
            else:
                print("\nPathPilot: Available job descriptions:")
                for j in jobs:
                    print(f"  - {j}")
                print()
            continue

        if user_input.lower() == "weak topics":
            topics = get_weak_topics()
            if not topics:
                print("\nPathPilot: No weak topics recorded yet.\n")
            else:
                print("\nPathPilot: Here are your current weak topics:")
                for t in topics:
                    print(f"  - {t['topic']} / {t['concept']} (attempts: {t['attempts']}, correct: {t['correct']})")
                print()
            continue

        if user_input.lower().startswith("mistake:"):
            try:
                content = user_input.split("mistake:", 1)[1].strip()
                topic, concept = [x.strip() for x in content.split("|")]
                result = record_mistake(topic, concept)
                print(f"\nPathPilot: {result}\n")
            except ValueError:
                print("\nFormat: mistake: <topic> | <concept>\n")
            continue

        if user_input.lower().startswith("improved:"):
            try:
                content = user_input.split("improved:", 1)[1].strip()
                topic, concept = [x.strip() for x in content.split("|")]
                result = mark_as_improved(topic, concept)
                print(f"\nPathPilot: {result}\n")
            except ValueError:
                print("\nFormat: improved: <topic> | <concept>\n")
            continue

        if user_input.lower().startswith("study:"):
            try:
                content = user_input.split("study:", 1)[1].strip()
                filename, question = [x.strip() for x in content.split("|", 1)]
                note_content = load_note(filename)

                if note_content is None:
                    print(f"\nPathPilot: Couldn't find '{filename}' in data/notes/. Type 'notes' to see available files.\n")
                    continue

                print("\nPathPilot is thinking...\n")
                answer = ask_pathpilot_with_notes(question, note_content)
                print(f"PathPilot: {answer}\n")
            except ValueError:
                print("\nFormat: study: <filename> | <question>\n")
            continue

        if user_input.lower().startswith("quiz:"):
            filename = user_input.split("quiz:", 1)[1].strip()
            note_content = load_note(filename)

            if note_content is None:
                print(f"\nPathPilot: Couldn't find '{filename}' in data/notes/. Type 'notes' to see available files.\n")
                continue

            print("\nPathPilot is generating a quiz...\n")
            quiz_question = "Generate 3 short quiz questions (with answers) based on this material to test my understanding."
            answer = ask_pathpilot_with_notes(quiz_question, note_content)
            print(f"PathPilot: {answer}\n")
            continue

        if user_input.lower().startswith("career:"):
            filename = user_input.split("career:", 1)[1].strip()
            job_desc = load_job_description(filename)

            if job_desc is None:
                print(f"\nPathPilot: Couldn't find '{filename}' in data/career/. Type 'jobs' to see available files.\n")
                continue

            print("\nPathPilot is analyzing this opportunity...\n")
            answer = ask_pathpilot_career(job_desc)
            print(f"PathPilot: {answer}\n")
            continue

        if user_input.lower().startswith("skillgap:"):
            content = user_input.split("skillgap:", 1)[1].strip()
            if " vs " not in content.lower():
                print("\nFormat: skillgap: <skill1> vs <skill2>\n")
                continue

            skills = [s.strip() for s in content.split(" vs ")]
            print("\nPathPilot is comparing your options...\n")
            answer = ask_pathpilot_skillgap(skills)
            print(f"PathPilot: {answer}\n")
            continue

        # Default: normal question to the AI agent (uses profile + memory only)
        print("\nPathPilot is thinking...\n")
        try:
            answer = ask_pathpilot(user_input)
            print(f"PathPilot: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()