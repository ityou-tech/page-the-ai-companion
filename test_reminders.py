from src.ai_companion.reminders import get_reminders
print(f"Number of reminders: {len(get_reminders())}")
print("Reminders:")
for i, reminder in enumerate(get_reminders(), 1):
    print(f"{i}. {reminder.get('text', '')} (at {reminder.get('timestamp', 'unspecified')})")