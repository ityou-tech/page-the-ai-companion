"""Core chat functionality for AI Companion."""

import re

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from src.ai_companion.config import DEFAULT_MODEL, SYSTEM_MESSAGE
from src.ai_companion.reminders import extract_reminder, save_reminder


class ChatSession:
    """Manages a chat session with the AI companion."""
    
    def __init__(self, model_name=None):
        """Initialize a new chat session.
        
        Args:
            model_name (str, optional): Name of the Ollama model to use
        """
        # Initialize chat model
        self.model_name = model_name or DEFAULT_MODEL
        self.llm = ChatOllama(model=self.model_name)
        
        # Initialize chat history
        self.history = InMemoryChatMessageHistory()
        
        # Add system message
        system_message = SystemMessage(content=SYSTEM_MESSAGE)
        self.history.add_message(system_message)
    
    def process_input(self, user_input):
        """Process user input, checking for reminders and generating a response.
        
        Args:
            user_input (str): The raw user input text
            
        Returns:
            str: The AI's response
        """
        # Check if this is a request to list reminders
        if re.search(r"list (all |my |)(reminders|tasks|todos)", user_input.lower()):
            from src.ai_companion.reminders import get_reminders
            reminders = get_reminders()
            
            if not reminders:
                response_text = "You don't have any reminders saved yet."
            else:
                response_text = "Sure thing! Here are the reminders I have for you:\n"
                for i, reminder in enumerate(reminders, 1):
                    text = reminder.get("text", "")
                    timestamp = reminder.get("timestamp", "unspecified time")
                    response_text += f"{i}. {text} (at {timestamp})\n"
            
            # Add to history
            self.history.add_message(HumanMessage(content=user_input))
            self.history.add_message(AIMessage(content=response_text))
            
            return response_text
        
        # Check for new reminders
        reminder, timestamp = extract_reminder(user_input)
        if reminder:
            save_reminder(reminder, timestamp)
        
        # Skip empty inputs
        if not user_input.strip():
            return None
        
        # Add to history and get response
        self.history.add_message(HumanMessage(content=user_input))
        response = self.llm.invoke(self.history.messages)
        
        # Save the response to history
        self.history.add_message(AIMessage(content=response.content))
        
        return response.content
    
    def get_history(self):
        """Get the current conversation history.
        
        Returns:
            list: List of message objects
        """
        return self.history.messages


def start_interactive_chat():
    """Start an interactive chat session in the terminal."""
    session = ChatSession()
    
    print("🧠 Page is ready. Say something! (Press Ctrl+C to quit)\n")
    
    try:
        while True:
            user_input = input("You: ")
            response = session.process_input(user_input)
            
            if response:
                print("Page:", response)
    except KeyboardInterrupt:
        print("\nGoodbye! Thanks for chatting with Page.")