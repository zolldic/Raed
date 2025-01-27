#!/usr/bin/env python3
"""
This module contains the implementation of the task for writing a full proposal
using the Telegram bot framework.

Functions:
    write_proposal_task(update: Update, context: ContextTypes.DEFAULT_TYPE): Asynchronously handles the task of writing a full proposal based on user input and profile data.
"""


from telegram import Update
from telegram.ext import ContextTypes
from logging import getLogger
from ...utils.gemini import generate_full_proposal
from ... import CHOOSE_TASK

logger = getLogger(__name__)


async def write_proposal_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Asynchronously handles the task of writing a full proposal based on user input and profile data.

    Args:
        update (telegram.Update): The update object that contains the incoming update.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other context-specific information.

    Returns:
        int: return to CHOOSE_TASK conversation state
    """

    text: str = update.message.text
    profile = context.user_data["profile"]

    response = generate_full_proposal(text, profile)
    await update.message.reply_text(
        response,
        parse_mode='HTML'
    )
    logger.info("Full proposal generated for user")
    return CHOOSE_TASK
