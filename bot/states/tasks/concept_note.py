#!/usr/bin/env python3
"""
This module contains the task for creating a concept note using the Telegram bot.

Functions:
    create_note_task(update: Update, context: ContextTypes.DEFAULT_TYPE)
        Asynchronously handles the creation of a concept note based on user input and profile data.
"""


from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from ...utils.gemini import generate_concept_note
from ...utils.utilties import define_language


async def create_note_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Asynchronously handles the creation of a concept note based on user input and profile data.

    Args:
        update (telegram.Update): The update object that contains the message data.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.

    Returns:
        int: The state of the conversation handler, indicating the end of the conversation.
    """

    input = update.message.text
    profile = context.user_data["profile"]

    response = generate_concept_note(input, profile)
    await update.message.reply_text(
        f"""<b>Concept note:</b>
        {response}
        """,
        parse_mode='HTML'
    )
    html_text = define_language('end', context.user_data['language_code'])
    await update.message.reply_text(
        html_text,
        parse_mode='HTML'
    )
    return ConversationHandler.END
