#!/usr/bin/env python3
"""
This module contains the implementation of the task for writing a full proposal
using the Telegram bot framework.

Functions:
    write_proposal_task(update: Update, context: ContextTypes.DEFAULT_TYPE): Asynchronously handles the task of writing a full proposal based on user input and profile data.
"""


from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from ...utils.gemini import generate_full_proposal

from ...utils.utilties import define_language


async def write_proposal_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Asynchronously handles the task of writing a full proposal based on user input and profile data.

    Args:
        update (telegram.Update): The update object that contains the incoming update.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other context-specific information.

    Returns:
        int: The end state of the conversation handler.
    """

    input = update.message.text
    profile = context.user_data["profile"]

    response = generate_full_proposal(input, profile)
    await update.message.reply_text(
        f"""<b>Full Proposal:</b>
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
