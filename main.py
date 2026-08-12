from app.agent import ask_pathpilot
from app.memory import record_mistake, mark_as_improved, get_weak_topics


def print_help():
    print("\nCommands:")
    print("  Just type your question to ask PathPilot")
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

        # Default: normal question to the AI agent
        print("\nPathPilot is thinking...\n")
        try:
            answer = ask_pathpilot(user_input)
            print(f"PathPilot: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()