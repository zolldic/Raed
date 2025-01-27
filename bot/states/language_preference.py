#!/usr/bin/env pythono3
"""This module handles the language preference setting for the user in a Telegram bot.

Functions:
    set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Handles the language preference setting for the user.
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils.utilties import define_lang

from .. import CHOICE, SET_LANGUAGE

from logging import getLogger

logger = getLogger(__name__)


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the language preference setting for the user.

    This function is called when the user selects a language preference. It validates the user's input and sets the language code in the user's context data. If the input is invalid, it prompts the user to select a valid language. Once a valid language is selected, it sends a message to the user asking them to identify themselves as either an activist or representing an organization.

    Args:
        update (telegram.Update): The update object that contains the user's message.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other context-specific information.

    Returns:
        int: The next state in the conversation, either SET_LANGUAGE if the input is invalid or CHOICE if the language is successfully set.
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

        logger.info("Invalid language preference entered.")

        return SET_LANGUAGE

    if update.message.text == 'English':
        context.user_data['language_code'] = 'en'
    else:
        context.user_data['language_code'] = 'ar'

    conversation: dict[str] = {
        'en': ''.join((
            "<b>Thank you for choosing your preferred language!</b>\n",
            "Now, please let us know who you are. Are you an activist or representing an organization?",
            "\n\n<b>Options:</b>",
            "\n- Type 'Activist' if you are an individual activist.",
            "\n- Type 'Organization' if you are representing an organization.",
            "\n\nChoose an option to proceed."
        )),

        'ar': ''.join((
            "<b>شكرًا لاختيارك اللغة المفضلة!</b>\n",
            "الآن، يرجى إخبارنا عن هويتك. هل أنت ناشط أم تمثل منظمة؟",
            "\n\n<b>الخيارات:</b>",
            "\n- اكتب 'Activist' إذا كنت ناشطًا.",
            "\n- اكتب 'Organization' إذا كنت تمثل منظمة.",
            "\n\nاختر خيارًا للمتابعة."
        ))
    }

    text: str = define_lang(
        conversation,
        context.user_data['language_code']
    )

    await update.message.reply_text(
        text,
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

    logger.info(
        f"Language preference set to {context.user_data['language_code']}.")
    return CHOICE
