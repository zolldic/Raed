#!/usr/bin/env python3
"""This module provides the Gemini class for interacting with the Gemini generative AI model.
"""
import google.generativeai as genai
from logging import getLogger
from ..config import GEMINI_KEY
from ..config import system_config

logger = getLogger(__name__)


class Gemini:
    """A class to configure and interact with the Gemini generative AI model.
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
        try:
            response = self._model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error: {e}")
            return None

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

    def generate_concept_note(self, user_input: str, profile: str) -> str:
        """Generates a concept note based on the user's input and profile data.

        Args:
            user_input(str): The user's input for the concept note.
            profile(str): The user's profile data.
        Returns:
            str: The generated concept note.
        """
        prompt = ''.join(
            (
                "Generate a concept note based on the user’s input and profile data. Include the following elements:"
                "<b>Introduction (Context):</b> Provide background and context about the project."
                "<b>The Problem:</b> Describe the specific problem that needs to be addressed."
                "<b>General Goal:</b> State the overall goal of the project."
                "<b>Objectives/Goals:</b> List the specific objectives that support the general goal."
                "<b>Target Audience:</b> Identify the primary beneficiaries and stakeholders of the project."
                "<b>Expected Outcome:</b> Detail the anticipated results and impact of the project."
                f"User's input: ``{user_input}``"
                f"User's profile: ``{profile}``"
            )
        )
        response = self._model.generate_content(prompt)
        return response.text

    def generate_full_proposal(self, user_input: str, profile: str) -> str:
        """Generates a full proposal based on the user's input and profile data.

        Args:
            user_input(str): The user's input for the concept note.
            profile(str): The user's profile data.
        Returns:
            str: The generated proposal.
        """
        prompt = ''.join(
            (
                 "Generate a full proposal based on the user’s input and profile data. Include the following elements:"
                "<b>Introduction (Context):</b> Provide background and context about the project."
                "<b>Project Importance:</b> Explain why the project is important and its relevance."
                 "<b>The Problem:</b> Describe the specific problem that needs to be addressed."
                "<b>General Goal:</b> State the overall goal of the project."
                "<b>Objectives/Goals:</b> List the specific objectives that support the general goal."
                "<b>Target Audience:</b> Identify the primary beneficiaries and stakeholders of the project."
                "<b>Activities:</b> Outline the activities that will be implemented to reach the objectives."
                "<b>Expected Outcome:</b> Detail the anticipated results and impact of the project."
                "<b>Partnerships:</b> Explain any partnerships or collaborations involved."
                "<b>Sustainability:</b> Outline how the project will be sustained over time."
                f"User's input: ``{user_input}``"
                f"User's profile: ``{profile}``"
            )
        )
        response = self._model.generate_content(prompt)
        return response.text


Model = Gemini(instruction=system_config)
