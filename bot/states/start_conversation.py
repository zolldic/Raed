#!/usr/bin/env python3
"""Module for starting the conversation with the user
    and determining if they are an activist or an organization.
"""
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    User
)
from telegram.ext import ContextTypes
from .. import CHOICE
from ..utils.utilties import define_language


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and determines the user's type (activist or organization).

    This function initiates the conversation with the user, determines if the user
    identifies as an activist or an organization, and saves user information such as
    username, language code, and chat ID to the database.

    Args:
        update (telegram.Update): The update object that contains information about
            the incoming message and its metadata.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that
            contains user-specific data for the conversation.

    Returns:
        int: The next conversation state.
    """

    user: User = update.effective_user

    context.user_data['id'] = user.id
    context.user_data['full_name'] = user.full_name
    context.user_data['username'] = user.username
    context.user_data['language_code'] = user.language_code

    html_text: str = define_language('start', user.language_code)
    await update.message.reply_text(
        html_text,
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(

            [[
                'English',
                'Arabic'
            ]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )

    return CHOICE
