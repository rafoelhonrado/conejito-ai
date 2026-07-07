"""
agent.py

Command-line interface for the local AI finance assistant.
"""

from db import create_database
from parser import parse_user_message
from router import execute


def main():
    create_database()

    print("Finance Agent Ready")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        user_message = input("\n> ").strip()

        if user_message.lower() in ["exit", "quit"]:
            print("Goodbye.")
            break

        if not user_message:
            continue

        try:
            action_obj = parse_user_message(user_message)

            print("\nACTION")
            print(action_obj)

            result = execute(action_obj)

            print("\nRESULT")
            print(result)

        except Exception as e:
            print("\nERROR")
            print(e)


if __name__ == "__main__":
    main()
