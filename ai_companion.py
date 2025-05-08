#!/usr/bin/env python3
"""
AI Companion - Main entry point.

This script provides a convenient entry point to start the AI Companion
without having to invoke the module directly.
"""

import sys
from src.ai_companion.cli import main

if __name__ == "__main__":
    sys.exit(main())