#!/usr/bin/env python3
"""This module provides utility functions for language definition and text extraction from PDF files.

Functions:
    define_language(state, user_language) -> str:
        Defines the language based on the user's language preference and conversation state.

    extract_text(path) -> str:
        Extracts and returns text content from a PDF file located at the given path.
"""
from ..config import conversation_states
import pypdf


def define_language(state, user_language) -> str:
    """
    Defines the language based on the user's language preference and conversation state.

    Args:
        state (str): The current state of the conversation.
        user_language (str): The language preference of the user ('en' for English, 'ar' for Arabic).

    Returns:
        str: The language-specific conversation state.
    """
    return (
        conversation_states[state]['en']
        if user_language == 'en'
        else conversation_states[state]['ar']
    )


def extract_text(path):
    """
    Extracts and returns text content from a PDF file located at the given path.

    Args:
        path (str): The file path to the PDF document.

    Returns:
        str: The extracted text content from the PDF.
    """
    text = ""
    with open(path, "rb") as f:
        reader = pypdf.PdfReader(f)

        for page in reader.pages:
            text += page.extract_text()
    return text
