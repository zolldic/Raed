#!/usr/bin/env python3
"""
This module contains the fallback state handler for a Telegram bot.
Functions:
    cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Handles the cancellation of the conversation and sends a goodbye message.
"""


from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler

)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the cancellation of the conversation and sends a goodbye message.
    Args:
        update (telegram.Update): The update object that contains the incoming update.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains data related to the update.
    Returns:
        int: The end state of the conversation.
    """
    await update.message.reply_text("GoodBye!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
