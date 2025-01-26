#!/usr/bin/env python3
"""This module handles the user's choice of role (Activist or Organization) in a Telegram bot conversation.

Functions:
    user_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Handles the user's choice of role and prompts them for the next action.
"""


import logging

from telegram import (
    Update,
    ReplyKeyboardMarkup
)

from telegram.ext import ContextTypes
from .. import CHOICE, CHOOSE_TASK, UPLOAD_PROFILE

from ..utils.utilties import define_language

logger = logging.getLogger(__name__)


async def user_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the user's choice of role
        (Activist or Org) and prompts them for the next action.\

            Args:
                update (telegram.Update): Incoming update from the user.
                context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context object containing user data.
            Returns:
                int: The next conversation state (CHOOSE_TASK, UPLOAD_PROFILE, or CHOICE).
    """

    user_type = update.message.text
    context.user_data['user_type'] = user_type

    if user_type == "Activist":
        html_text: str = define_language(
            'activist', context.user_data['language_code']
        )

        await update.message.reply_text(
            html_text,
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(
                [[
                    'Analyze a problem',
                    'Create a concept note',
                    'Write a full proposal'
                ]],
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )
        logger.info(f"User selected {user_type}. Proceeding to CHOOSE_TASK.")

        return CHOOSE_TASK
    elif user_type == "Organization":
        html_text: str = define_language(
            'organization', context.user_data['language_code']
        )
        await update.message.reply_text(
            html_text,
            parse_mode='HTML'
        )
        logger.info(
            f"User selected {user_type}. Proceeding to UPLOAD_PROFILE.")
        return UPLOAD_PROFILE
    else:
        html_text: str = define_language(
            'error_user_type', context.user_data['language_code'])
        await update.message.reply_text(
            html_text,
            parse_mode='HTML')
        logger.warning(f"Invalid choice entered by user: '{user_type}'")
        return CHOICE
