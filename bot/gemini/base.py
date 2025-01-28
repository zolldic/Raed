#!/usr/bin/env python3
"""This module provides the Gemini class for interacting with the Gemini generative AI model.
"""
from ..config import GEMINI_KEY
import google.generativeai as genai


class Gemini:
    """A class to configure and interact with the Gemini generative AI model.

    Attributes:
        _model (genai.GenerativeModel): An instance of the generative AI model.
    """

    def __init__(self, **kwargs: dict) -> None:
        """Initializes the Gemini class with the specified configuration.

        Args:
            **kwargs(dict): Optional keyword arguments for model configuration.
            - instruction(str, optional): System instruction for the generative model.
        """
        genai.configure(api_key=GEMINI_KEY)
        self._model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction=kwargs.get("instruction", None),
        )
