#!/usr/bin/env python3
""" """
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
