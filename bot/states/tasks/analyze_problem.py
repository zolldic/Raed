#!/usr/bin/env python3
"""
This module contains the task for analyzing a problem using the Telegram bot.

Functions:
    analyze_problem_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Handles the analysis of a problem provided by the user through a Telegram message.
"""


from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from ...utils.gemini import analyze_problem
from ...utils.utilties import define_language


async def analyze_problem_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the analysis of a problem provided by the user through a Telegram message.

    Args:
        update (telegram.Update): The update object that contains the message from the user.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.

    Returns:
        None
    """

    input = update.message.text
    context.user_data["problem"] = input
    response = analyze_problem(input)
    await update.message.reply_text(
        f"""<b>Problem Analysis</b>
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
