"""Command-line interface for AI Companion."""

import argparse
import sys

from src.ai_companion import __version__
from src.ai_companion.chat import ChatSession, start_interactive_chat
from src.ai_companion.config import DEFAULT_MODEL
from src.ai_companion.reminders import get_reminders


def start_chat_with_model(model_name):
    """Start an interactive chat session with the specified model.
    
    Args:
        model_name (str): Name of the Ollama model to use
    """
    session = ChatSession(model_name=model_name)
    print(f"🧠 Page is using model: {model_name}")
    print("Say something! (Press Ctrl+C to quit)\n")
    
    try:
        while True:
            user_input = input("You: ")
            response = session.process_input(user_input)
            
            if response:
                print("Page:", response)
    except KeyboardInterrupt:
        print("\nGoodbye! Thanks for chatting with Page.")


def parse_args():
    """Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="AI Companion - A personal chatbot with memory and reminders"
    )
    
    # General arguments
    parser.add_argument(
        "--version", action="version", version=f"AI Companion {__version__}"
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model to use (default: {DEFAULT_MODEL})"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Reminders command
    reminders_parser = subparsers.add_parser("reminders", help="Manage reminders")
    reminders_parser.add_argument(
        "--list", 
        action="store_true", 
        help="List all saved reminders"
    )
    
    return parser.parse_args()


def main():
    """Main entry point for the CLI."""
    args = parse_args()
    
    # If no command is specified, start chat
    if not args.command:
        start_chat_with_model(args.model)
        return 0
    
    # Handle reminders command
    elif args.command == "reminders" and args.list:
        reminders = get_reminders()
        if not reminders:
            print("No reminders found.")
            return 0
            
        print(f"Found {len(reminders)} reminders:")
        for i, reminder in enumerate(reminders, 1):
            timestamp = reminder.get("timestamp", "unspecified time")
            text = reminder.get("text", "")
            created = reminder.get("created_at", "")
            print(f"{i}. {text} (created: {created})")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())