"""Tests for the reminders module."""

import unittest
from src.ai_companion.reminders import extract_reminder


class TestReminders(unittest.TestCase):
    """Test the reminders functionality."""

    def test_extract_reminder_with_time(self):
        """Test that reminders with time are correctly extracted."""
        test_cases = [
            ("remind me to take my meds at 8:00 PM", "take my meds at 8:00 PM", "8:00 PM"),
            ("remind me to call mom at 9 PM", "call mom at 9 PM", "9 PM"),
            ("remind me to check email at 10:30am", "check email at 10:30am", "10:30am"),
            ("remind me to go for a run at 7 AM", "go for a run at 7 AM", "7 AM"),
        ]

        for input_text, expected_text, expected_time in test_cases:
            reminder, timestamp = extract_reminder(input_text)
            self.assertEqual(reminder, expected_text)
            self.assertEqual(timestamp, expected_time)

    def test_extract_reminder_no_match(self):
        """Test that non-reminder text returns None."""
        test_cases = [
            "hello there",
            "what time is it?",
            "remind me about something",
        ]

        for input_text in test_cases:
            reminder, timestamp = extract_reminder(input_text)
            self.assertIsNone(reminder)
            self.assertIsNone(timestamp)


if __name__ == "__main__":
    unittest.main()