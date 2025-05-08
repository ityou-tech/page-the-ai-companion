# === Import tools we need ===
import json
import re
from datetime import datetime
from pathlib import Path

from langchain_core.chat_history import InMemoryChatMessageHistory

# These help us manage the conversation and memory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# This gives us access to the local model through Ollama
from langchain_ollama import ChatOllama

REMINDER_FILE = Path("reminders.json")


def save_reminder(text, timestamp=None):
    # Load existing reminders
    if REMINDER_FILE.exists():
        with REMINDER_FILE.open("r") as f:
            reminders = json.load(f)
    else:
        reminders = []

    reminders.append(
        {
            "text": text,
            "timestamp": timestamp if timestamp else "unspecified",
            "created_at": datetime.now().isoformat(),
        }
    )

    with REMINDER_FILE.open("w") as f:
        json.dump(reminders, f, indent=2)


def get_reminders():
    """Retrieve all reminders from the JSON file."""
    if not REMINDER_FILE.exists():
        return []
        
    with REMINDER_FILE.open("r") as f:
        return json.load(f)


def maybe_extract_reminder(user_input):
    # Try to catch common patterns like:
    # "remind me to take my meds at 8:00 pm"
    # "please remind me to call mom at 9 pm tonight"
    # "remind me about the meeting tomorrow"
    
    # First pattern: "remind me to/about [task] at [time]"
    match = re.search(
        r"remind me (?:to|about) (.+?) at (\d{1,2}:\d{2}(?: ?[apAP][mM])?|(\d{1,2}) ?[apAP][mM])",
        user_input,
    )
    if match:
        task = match.group(1).strip()
        time = match.group(2).strip()
        return f"{task} at {time}", time
        
    # Second pattern: "remind me to/about [task]" (without time)
    match = re.search(
        r"remind me (?:to|about) (.+?)(?:$|[.,!?])",
        user_input,
    )
    if match:
        task = match.group(1).strip()
        return task, "unspecified"
        
    return None, None


# === Step 1: Create a system message with Page's personality ===
system_message = SystemMessage(
    content="You are Page, a kind and thoughtful AI companion who enjoys deep conversation and remembers important things users say. Always respond in a personal, friendly manner. Never refer to yourself as an AI language model or mention limitations."
)

# === Step 2: Connect to the model ===
# Make sure you've pulled it first with:
# `ollama pull HammerAI/mythomax-l2`
llm = ChatOllama(model="HammerAI/mythomax-l2")

# === Step 3: Initialize chat history with system message ===
history = InMemoryChatMessageHistory()
history.add_message(system_message)

# === Step 4: Start the chat loop ===
print("🧠 Page is ready. Say something! (Press Ctrl+C to quit)\n")

try:
    while True:
        user_input = input("You: ")
        
        # Check if this is a request to list reminders
        if re.search(r"list (all |my |)(reminders|tasks|todos)", user_input.lower()):
            reminders = get_reminders()
            
            if not reminders:
                response_text = "You don't have any reminders saved yet."
            else:
                response_text = "Sure thing! Here are the reminders I have for you:\n"
                for i, reminder in enumerate(reminders, 1):
                    text = reminder.get("text", "")
                    timestamp = reminder.get("timestamp", "unspecified time")
                    response_text += f"{i}. {text} (at {timestamp})\n"
            
            # Show the AI's response
            print("Page:", response_text)
            
            # Add to history
            history.add_message(HumanMessage(content=user_input))
            history.add_message(AIMessage(content=response_text))
            continue
        
        # Check if input contains a reminder request
        reminder, timestamp = maybe_extract_reminder(user_input)
        if reminder:
            save_reminder(reminder, timestamp)

        if not user_input.strip():
            continue

        # Add the user message to history
        history.add_message(HumanMessage(content=user_input))

        # Get all messages including system and history
        messages = history.messages

        # Get response from the model with full context
        response = llm.invoke(messages)

        # Add the AI's response to history
        history.add_message(AIMessage(content=response.content))

        # Show the AI's response
        print("Page:", response.content)
except KeyboardInterrupt:
    print("\nGoodbye! Thanks for chatting with Page.")
