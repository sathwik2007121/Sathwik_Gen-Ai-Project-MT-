"""
test_interactive.py — Interactive policy advisor testing CLI.

Run:
    python test_interactive.py
"""

from __future__ import annotations

import sys
from rag import answer

def main():
    print("=" * 65)
    print("🎓 Mirai University Academic & Hostel Policy Advisor")
    print("   Type any question below, or type 'exit' or 'q' to quit.")
    print("=" * 65)

    if len(sys.argv) > 1:
        # CLI argument mode
        q = " ".join(sys.argv[1:])
        print(f"\nQuestion: {q}")
        res = answer(q)
        print(f"\nAnswer  : {res['answer']}")
        print(f"Sources : {res['sources'] if res['sources'] else 'N/A'}\n")
        return

    while True:
        try:
            user_input = input("\nAsk a question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break

        print("\nSearching policy handbook...")
        try:
            result = answer(user_input)
            print("-" * 65)
            print(f"Answer : {result['answer']}")
            sources_str = ", ".join(f"page {p}" for p in result["sources"]) if result["sources"] else "None (unsupported/not found)"
            print(f"Sources: {sources_str}")
            print("-" * 65)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
