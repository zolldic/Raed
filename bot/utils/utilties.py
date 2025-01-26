#!/usr/bin/env python3
""" """
from ..config import conversation_states
import pypdf


def define_language(state, user_language) -> str:
    """ """
    return (
        conversation_states[state]['en']
        if user_language == 'English'
        else conversation_states[state]['ar']
    )


def extract_text(path):
    text = ""
    with open(path, "rb") as f:
        reader = pypdf.PdfReader(f)

        for page in reader.pages:
            text += page.extract_text()
    return text
