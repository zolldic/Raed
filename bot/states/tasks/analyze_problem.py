#!/usr/bin/env python3
"""
This module contains the task for analyzing a problem using the Telegram bot.

Functions:
    analyze_problem_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Handles the analysis of a problem provided by the user through a Telegram message.
"""


from telegram import Update
from telegram.ext import ContextTypes
from ... import CHOOSE_TASK
from ...utils.gemini import analyze_problem
from logging import getLogger


logger = getLogger(__name__)


async def analyze_problem_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handles the analysis of a problem provided by the user through a Telegram message.

    Args:
        update (telegram.Update): The update object that contains the message from the user.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.

    Returns:
        int: return to CHOOSE_TASK conversation state
    """

    text: str = update.message.text
    context.user_data["problem"] = text
    response: str = analyze_problem(text)

    await update.message.reply_text(
        response,
        parse_mode='HTML'
    )
    logger.info(
        f"Problem analyzed for user {update.effective_user.name}: {text}")
    return CHOOSE_TASK
