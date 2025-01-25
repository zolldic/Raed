#!/usr/bin/python3
""" """
import google.generativeai as genai
from ..config import GEMINI_KEY
from ..config import instruction


genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    "gemini-1.5-flash", system_instruction=instruction)


def analyze_problem(text):
    """ """
    prompt = f"""
    You are an expert in social problem analysis using the Problem Tree method.
    Your task is to analyze the given social problem `{text}`
    and break it down into its core components.
    Core Problem (Trunk): Identify the central issue or challenge described. Define it clearly and concisely.
    Causes (Roots): Determine the underlying causes of the problem. Focus on both direct and indirect causes that contribute to the issue.
    Consequences (Branches): Explore the effects and consequences of the problem. Highlight how it impacts individuals, communities, or society at large.
    Use the following format for your response:
    Core Problem (Trunk): [Brief definition of the central problem]
    Causes (Roots):
    [Cause 1]
    [Cause 2]
    [Cause 3] (and so on, depending on the complexity)
    Consequences (Branches):
    [Consequence 1]
    [Consequence 2]
    [Consequence 3] (and so on)
    The user will provide a detailed description of the social problem. Ensure your response is logical, structured, and sensitive to the social context of the problem.
    """
    response = model.generate_content(prompt)
    return response.text


def generate_concept_note(text, profile):
    """ """

    prompt = f"""You are an expert in development and project proposal writing.
    Your task is to generate a professional concept note based on this user-provided information `{text}`.
    If the user has provided an organization profile ({profile}), you must align the concept note with this profile.
    Ensure the response is tailored to the organization’s priorities and values.
    The concept note should include the following sections:
    Introduction (Context): Provide a brief overview of the context surrounding the project. Explain the social, economic, or cultural background that makes the project relevant and necessary.
    The Problem: Clearly define the main social problem the project seeks to address. Use evidence or examples to highlight its significance and impact.
    Theory of Change: Explain the proposed approach to solving the problem. Describe how specific actions will lead to desired changes and outcomes.
    General Goal: State the overall purpose of the project. This should be a broad and visionary statement about the long-term impact the project aims to achieve.
    Objective Goals: Break down the general goal into smaller, measurable objectives that are specific, actionable, and time-bound.
    Target Audience: Identify and describe the primary beneficiaries of the project. Include key demographic details (e.g., age, gender, location) and explain why this group is the focus.
    Expected Outcomes: Outline the anticipated results of the project. These should be clear, tangible, and aligned with the objectives and theory of change.
    <b>Introduction (Context):</b> [Content here]
    <b>The Problem:</b> [Content here]
    <b>Theory of Change:</b> [Content here]
    <b>General Goal:</b> [Content here]
    <b>Objective Goals:</b>
    [Objective 1]
    [Objective 2]
    [Objective 3] (and so on)
    <b>Target Audience:</b> [Content here]
    <b>Expected Outcomes:</b>
    [Outcome 1]
    [Outcome 2]
    [Outcome 3] (and so on)
    Make sure your response is concise, logical, and easy to understand.     
    """
    response = model.generate_content(prompt)
    return response.text


def generate_full_proposal(text, profile):
    prompt = f"""
You are an expert in development and project proposal writing.  
Your task is to generate a professional full proposal based on this user-provided information `{text}`.  
If the user has provided an organization profile ({profile}), you must align the proposal with this profile.  
Ensure the response is tailored to the organization’s priorities, values, and sector of focus.  

The full proposal should include the following sections:  

1. **Introduction (Context):** Provide a detailed overview of the context surrounding the project. Explain the social, economic, or cultural background that makes the project relevant and necessary.  
2. **The Problem:** Clearly define the main social problem the project seeks to address. Use evidence or examples to highlight its significance and impact.  
3. **Theory of Change:** Explain the proposed approach to solving the problem. Describe how specific actions will lead to desired changes and outcomes.  
4. **General Goal:** State the overall purpose of the project. This should be a broad and visionary statement about the long-term impact the project aims to achieve.  
5. **Objective Goals:** Break down the general goal into smaller, measurable objectives that are specific, actionable, and time-bound.  
6. **Target Audience:** Identify and describe the primary beneficiaries of the project. Include key demographic details (e.g., age, gender, location) and explain why this group is the focus.  
7. **Activities:** Provide a brief description of the key activities that will be undertaken to achieve the objectives. Highlight the most critical steps in the implementation process.  
8. **Risk Assessment:** Identify potential risks that could impact the success of the project. Describe these risks and propose strategies to mitigate them.  
9. **Assumptions:** List any assumptions being made about the project’s success, resources, stakeholders, or context. Ensure these assumptions are realistic and relevant.  
10. **Challenges:** Outline the anticipated challenges that may arise during the project implementation. Provide solutions or approaches to address these challenges effectively.  
11. **Expected Outcomes:** Clearly outline the anticipated results of the project. These should be specific, measurable, and aligned with the objectives and theory of change.  

Your response should use the following structure:  

<b>Introduction (Context):</b> [Content here]  
<b>The Problem:</b> [Content here]  
<b>Theory of Change:</b> [Content here]  
<b>General Goal:</b> [Content here]  
<b>Objective Goals:</b>  
  - [Objective 1]  
  - [Objective 2]  
  - [Objective 3] (and so on)  
<b>Target Audience:</b> [Content here]  
<b>Activities:</b>  
  - [Activity 1]  
  - [Activity 2]  
  - [Activity 3] (and so on)  
<b>Risk Assessment:</b> [Content here]  
<b>Assumptions:</b> [Content here]  
<b>Challenges:</b> [Content here]  
<b>Expected Outcomes:</b>  
  - [Outcome 1]  
  - [Outcome 2]  
  - [Outcome 3] (and so on)  

Make sure your response is comprehensive, concise, logical, and easy to understand. If additional clarification is needed, request more information from the user before completing the proposal.
    """
    response = model.generate_content(prompt)
    return response.text
