"""Reminder system for AI Companion."""

import json
import re
from datetime import datetime

from src.ai_companion.config import REMINDER_FILE


def save_reminder(text, timestamp=None):
    """Save a reminder to the JSON file.
    
    Args:
        text (str): The reminder text
        timestamp (str, optional): When the reminder is for
    """
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
    """Retrieve all reminders from the JSON file.
    
    Returns:
        list: List of reminder dictionaries
    """
    if not REMINDER_FILE.exists():
        return []
        
    with REMINDER_FILE.open("r") as f:
        return json.load(f)


def extract_reminder(user_input):
    """Try to extract reminder information from user input.
    
    Args:
        user_input (str): The raw user input text
        
    Returns:
        tuple: (reminder_text, timestamp) or (None, None) if no reminder detected
    """
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