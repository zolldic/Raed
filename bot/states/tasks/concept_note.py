#!/usr/bin/env python3
"""
This module contains the task for creating a concept note using the Telegram bot.

Functions:
    create_note_task(update: Update, context: ContextTypes.DEFAULT_TYPE)
        Asynchronously handles the creation of a concept note based on user input and profile data.
"""


from telegram import Update
from telegram.ext import ContextTypes
from logging import getLogger
from ...utils.gemini import generate_concept_note
from ... import CHOOSE_TASK

logger = getLogger(__name__)


async def create_note_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Asynchronously handles the creation of a concept note based on user input and profile data.

    Args:
        update (telegram.Update): The update object that contains the message data.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.

    Returns:
        int: return to CHOOSE_TASK conversation state.
    """

    text: str = update.message.text
    profile = context.user_data["profile"]

    response = generate_concept_note(text, profile)
    await update.message.reply_text(

        response,
        parse_mode='HTML'
    )
    logger.info("Concept note created successfully for user")
    return CHOOSE_TASK
