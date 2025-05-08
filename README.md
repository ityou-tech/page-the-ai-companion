# AI Companion

A personal AI companion chatbot that uses local LLM models through Ollama with memory and reminder capabilities.

## Features

- **Conversational AI**: Chat with "Page", a friendly AI companion powered by local LLM models
- **Conversation Memory**: Page remembers your conversation history during a session
- **Reminder System**: Ask Page to remind you of tasks (e.g., "remind me to take my meds at 8:00 pm")
- **CLI Interface**: Simple command-line interface for chatting and managing reminders
- **Configuration Options**: Customize the model and behavior through environment variables

## Prerequisites

- Python 3.13 or higher
- [Ollama](https://ollama.ai/) installed on your system
- [uv](https://github.com/astral-sh/uv) - a fast Python package installer and resolver

## Setup and Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ai-companion.git
   cd ai-companion
   ```

2. Pull the required LLM model:
   ```bash
   ollama pull HammerAI/mythomax-l2
   ```

3. Install the package with uv:
   ```bash
   uv pip install -e .
   ```

## Usage

### Starting a Chat Session

You can start chatting with Page:

```bash
# Using the default model
uv run ai-companion

# Specify a different model
ollama pull llama3.2:latest
uv run ai-companion --model llama3.2:latest
```

Type your messages and press Enter to send them. Page will respond based on the conversation context.

### Managing Reminders

During a chat, set reminders by using phrases like:
- "remind me to take my meds at 8:00 pm"
- "remind me to call mom at 9 PM"

To view all your saved reminders:

```bash
uv run ai-companion reminders --list
```

Reminders are saved to a local file in `~/.ai_companion/data/reminders.json`.

### Running the Development Script

You can also run the companion using the development script:

```bash
python ai_companion.py
```

## Development

### Project Structure

The project is structured as follows:

```
ai-companion/
├── src/
│   └── ai_companion/            # Main package
│       ├── __init__.py          # Package initialization
│       ├── chat.py              # Core chat functionality
│       ├── cli.py               # Command-line interface
│       ├── config.py            # Configuration settings
│       └── reminders.py         # Reminder system
├── ai_companion.py              # Entry point script
├── pyproject.toml               # Project configuration
├── README.md                    # Documentation
├── .gitignore                   # Git ignore file
└── .python-version              # Python version file
```

### Configuration Options

You can customize the AI Companion by setting these environment variables:

- `AI_COMPANION_MODEL`: The Ollama model to use (default: "HammerAI/mythomax-l2")

### Development Setup

For development work:

```bash
# Install development dependencies
uv pip install -e ".[dev]"

# Format code
uv run black .
uv run isort .

# Run linter
uv run ruff .

# Run tests (when implemented)
uv run pytest
```

## Why uv?

[uv](https://github.com/astral-sh/uv) offers several advantages over traditional package managers:

- **Speed**: Significantly faster than pip for installations
- **No Manual Activation**: Run commands directly with `uv run` without activating virtual environments
- **Reliability**: Improved dependency resolution
- **Lockfile Support**: Automatic generation of `uv.lock` for reproducible environments
- **Isolation**: Better virtual environment management

## Troubleshooting

### Common Issues

If you encounter build errors, make sure:
1. The Ollama service is running before starting the chat
2. You've pulled the needed model (like MythoMax-L2) with Ollama

### Model Alternatives

You can use any model supported by Ollama:

```bash
# List available models
ollama list

# Use a different model
ai-companion chat --model llama3:8b
```

## License

This project is licensed under the MIT License.