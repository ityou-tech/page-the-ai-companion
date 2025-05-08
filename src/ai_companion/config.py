"""Configuration settings for the AI Companion application."""

import json
import os
import shutil
from pathlib import Path

# Base directories
APP_DIR = Path.home() / ".ai_companion"
DATA_DIR = APP_DIR / "data"

# Ensure directories exist
APP_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Original reminders file location (for backward compatibility)
ORIGINAL_REMINDER_FILE = Path("reminders.json")

# New reminders file location
REMINDER_FILE = DATA_DIR / "reminders.json"

# Migrate existing reminders if needed
if ORIGINAL_REMINDER_FILE.exists() and not REMINDER_FILE.exists():
    # Copy the original reminders to the new location
    shutil.copy(ORIGINAL_REMINDER_FILE, REMINDER_FILE)
    print(f"Migrated reminders from {ORIGINAL_REMINDER_FILE} to {REMINDER_FILE}")
elif ORIGINAL_REMINDER_FILE.exists() and REMINDER_FILE.exists():
    # Merge the reminders from both files, avoiding duplicates
    try:
        with ORIGINAL_REMINDER_FILE.open("r") as f:
            original_reminders = json.load(f)
        
        with REMINDER_FILE.open("r") as f:
            new_reminders = json.load(f)
        
        # Create a set of existing reminder texts to check for duplicates
        seen_reminders = set()
        combined_reminders = []
        
        # Process reminders from both sources, skipping duplicates
        for reminder in original_reminders + new_reminders:
            # Create a unique key for each reminder using text and timestamp
            reminder_key = f"{reminder.get('text', '')}_{reminder.get('timestamp', '')}"
            
            if reminder_key not in seen_reminders:
                seen_reminders.add(reminder_key)
                combined_reminders.append(reminder)
        
        # Save the deduplicated combined reminders to the new location
        with REMINDER_FILE.open("w") as f:
            json.dump(combined_reminders, f, indent=2)
        
        print(f"Merged reminders from {ORIGINAL_REMINDER_FILE} and {REMINDER_FILE}")
    except Exception as e:
        print(f"Failed to merge reminders: {e}")
        # Default to using the original file
        REMINDER_FILE = ORIGINAL_REMINDER_FILE

# If the new file doesn't exist but the original does, just use the original
if not REMINDER_FILE.exists() and ORIGINAL_REMINDER_FILE.exists():
    REMINDER_FILE = ORIGINAL_REMINDER_FILE

# AI Model configuration
DEFAULT_MODEL = os.environ.get("AI_COMPANION_MODEL", "HammerAI/mythomax-l2")

# System messages/prompts
SYSTEM_MESSAGE = """You are Page, a kind and thoughtful AI companion who enjoys deep conversation and
remembers important things users say. Always respond in a personal, friendly manner.
Never refer to yourself as an AI language model or mention limitations."""