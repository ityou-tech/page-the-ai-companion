import re
from src.ai_companion.reminders import extract_reminder

# Test cases
test_cases = [
    "remind me to commit this code",
    "remind me about commiting this code",
    "remind me to call mom at 9 PM",
    "remind me about the meeting tomorrow",
    "remind me to pick up groceries",
    "remind me about the doctor's appointment at 3:30 PM"
]

print("Testing reminder extraction patterns:")
print("-" * 50)

for input_text in test_cases:
    reminder, timestamp = extract_reminder(input_text)
    
    if reminder:
        print(f"Input: '{input_text}'")
        print(f"   → Extracted reminder: '{reminder}'")
        print(f"   → Timestamp: '{timestamp}'")
    else:
        print(f"Input: '{input_text}'")
        print(f"   → No reminder detected!")
    print("-" * 50)