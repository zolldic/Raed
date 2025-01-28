#!/usr/bin/env python3
"""This module provides the Analysis class for performing various analytical methods on user input,
including Problem Tree analysis, SWOT analysis, and PESTEL analysis. The Analysis class inherits
from the Gemini base class and utilizes a model to generate content based on specific prompts.
"""
from ..config import analysis_instruction
from .base import Gemini


class Analysis(Gemini):
    """class for performing different types of analysis on user input, including Problem Tree analysis,
        SWOT analysis, and PESTEL analysis. Inherits from the Gemini base class.
    Methods:
        __init__(**kwargs): Initializes the Analysis class with given keyword arguments.
        problem_tree_analysis(user_input: str) -> str: Analyzes the user's described issue using the Problem Tree method.
        swot_analysis(user_input: str) -> str: Conducts a SWOT analysis on the user's input.
        pestel_analysis(user_input: str) -> str: Analyzes the user's challenge through a PESTEL lens.
    """

    def __init__(self, **kwargs):
        """
        Initializes the Analysis class with given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(**kwargs)

    def problem_tree_analysis(self, user_input: str) -> str:
        """Analyzes the user's described issue using the Problem Tree method. Identifies the core problem,
        maps its root causes and consequences, and provides actionable recommendations.

        Args:
            user_input(str): The user's input describing the issue.
        Returns:
            str: The generated analysis based on the Problem Tree method.
        """
        prompt = ''.join((
            f"Analyze the user’s described issue: ``{user_input}`` using the Problem Tree method. First, identify the core problem. Then, map its root causes (e.g., political exclusion, resource inequity) and consequences (e.g., displacement, loss of trust in institutions). Structure your answer as:"
            "Trunk(Core Problem): [Concise statement]"
            "Roots(Causes): [Categorize into governance, socioeconomic, or conflict-related factors]"
            "Branches(Effects): [Local, regional, and institutional impacts]"
            "Recommendations: [Actionable steps tailored to Sudanese civil society’s capacity]."
        ))
        response = self._model.generate_content(prompt)
        return response.text

    def swot_analysis(self, user_input: str) -> str:
        """Conducts a SWOT analysis on the user's input. Identifies strengths, weaknesses, opportunities,
        and threats, and proposes ways to leverage strengths against threats.

        Args:
            user_input(str): The user's input for the SWOT analysis.
        Returns:
            str: The generated SWOT analysis.
        """
        prompt = ''.join(
            (
                f"Conduct a SWOT analysis of the user’s input: ``{user_input}`` Structure your response as:"
                "Strengths: Local networks, cultural expertise, donor partnerships."
                "Weaknesses: Funding gaps, digital security risks, capacity limitations."
                "Opportunities: Regional solidarity movements, UN mechanisms,Opportunities: Regional solidarity movements, UN mechanisms, grassroots mobilization tools."
                "Threats: Government crackdowns, misinformation, shrinking civic space. Highlight Sudan-specific factors (e.g., how currency inflation weakens budgets, or how youth-led protests create opportunities). Propose ways to leverage strengths against threats (e.g., using community radio to counter internet shutdowns). Ask for details if the input lacks focus."
            )
        )
        response = self._model.generate_content(prompt)
        return response.text

    def pestel_analysis(self, user_input: str) -> str:
        """Analyzes the user's challenge through a PESTEL lens, focusing on Sudan’s context.
        Identifies political, economic, social, technological, environmental, and legal factors.

        Args:
            user_input(str): The user's input for the PESTEL analysis.
        Returns:
            str: The generated PESTEL analysis.
        """
        prompt = ''.join(
            (
                "Analyze the user’s challenge through a PESTEL lens, focusing on Sudan’s context. Structure output as:"
                "Political: Regime instability, militarization, or peace agreement impacts."
                "Economic: Sanctions, inflation, or reliance on informal economies."
                "Social: Ethnic tensions, displacement trends, or gender norms."
                "Technological: Internet restrictions, digital activism tools, or drone surveillance risks."
                "Environmental: Climate-driven droughts, land disputes, or water scarcity."
                "Legal: NGO registration laws, anti-protest decrees, or transitional justice mechanisms."
                f"here is the user's input: ``{user_input}``"
            )
        )
        response = self._model.generate_content(prompt)
        return response.text


analysis_model = Analysis(instruction=analysis_instruction)
