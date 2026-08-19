"""
cli_demo.py
===========
A tiny command-line version of the app, in case you don't want the web UI.

Run it with:   python cli_demo.py sample_data/sample.txt

Then type questions and press Enter. Type 'quit' to exit.
"""

import sys
from src.chatbot import DocumentChatbot


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python cli_demo.py <path-to-file.pdf|.txt|.md>")
        sys.exit(1)

    file_path = sys.argv[1]

    print("Loading AI models (first run downloads them, please wait)...")
    bot = DocumentChatbot()

    print(f"Reading and indexing '{file_path}'...")
    n = bot.add_file(file_path)
    print(f"Indexed {n} chunks. Ask me anything! (type 'quit' to exit)\n")

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if question.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break
        if not question:
            continue

        answer, sources = bot.ask(question)
        print(f"\nAI: {answer}\n")
        print(f"   (based on {len(sources)} matching passage(s))\n")


if __name__ == "__main__":
    main()
