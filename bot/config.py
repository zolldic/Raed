#!/usr/bin/env python3
"""
This module loads environment variables and configures the Gemini model.

Functions:
    load_dotenv: Loads environment variables from a .env file.
    os.getenv: Retrieves environment variables.

Environment Variables:
    BOT_KEY: API key for the bot.
    GEMINI_KEY: API key for the Gemini model.

Configuration:
    instruction: Tuple containing instructions for the Gemini model.
        - The first element specifies the role of the model as a civil society activist in Sudan specializing in writing concept notes and proposals for fundraising.
        - The second element specifies that responses should be in Arabic.
"""

from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()
BOT_KEY = os.getenv('API')
GEMINI_KEY = os.getenv("GEMINI_KEY")

# config gemini model
instruction = (
    "you're are a civil society activist in Sudan specialize in writing concept note and proposals for fund rising",
    f"your responses should be in Arabic"
)
