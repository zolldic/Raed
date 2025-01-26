#!/usr/bin/env pythono3
"""
This module handles the language preference state for a Telegram bot.

Functions:
    set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Handles the user's language preference input and updates the context with the selected language code.
        If the input is invalid, prompts the user to select a valid language (English or Arabic).
        Once a valid language is selected, prompts the user to choose their user type (Activist or Organization).
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils.utilties import define_language

from .. import CHOICE, SET_LANGUAGE


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the user's language preference selection.
        This function checks if the user's input is either 'English' or 'Arabic'. If the input is invalid,
        it prompts the user to select a valid language. If the input is valid, it sets the user's language
        preference in the context and prompts the user to select their user type.

    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object that contains user data.
    Returns:
        int: The next state of the conversation, either SET_LANGUAGE or CHOICE.
    """

    if (update.message.text != 'English'
            and update.message.text != 'Arabic'):
        await update.message.reply_text(
            f'<b> You entered {update.message.text}. Please select a valid language preference: either English or Arabic.</b>',
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(

                [[
                    'English',
                    'Arabic'
                ]],
                one_time_keyboard=True,
                resize_keyboard=True
            ),

        )
        return SET_LANGUAGE

    if update.message.text == 'English':
        context.user_data['language_code'] = 'en'
    else:
        context.user_data['language_code'] = 'ar'

    html_text: str = define_language(
        'user_type', context.user_data['language_code'])
    await update.message.reply_text(
        html_text,
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(
            [
                [
                    'Activist',
                    'Organization'
                ]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        ),

    )
    return CHOICE
