from app.agent import ask_pathpilot

def main():
    print("=" * 50)
    print("  PathPilot AI — Your Study & Career Assistant")
    print("=" * 50)
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("PathPilot: Goodbye! Keep growing 🚀")
            break

        if not question:
            continue

        print("\nPathPilot is thinking...\n")

        try:
            answer = ask_pathpilot(question)
            print(f"PathPilot: {answer}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()