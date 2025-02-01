#!/usr/bin/env pythono3
"""This module contains the user_choice state for the Raed bot.
    Functions:
    async def user_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Handles the user's language choice and prompts the next action.
"""

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from logging import getLogger

from ..utils.utilties import define_lang
from .. import USER_CHOICE_HANDLER, CONVERSATION_HANDLER


logger = getLogger(__name__)


async def user_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the user's language choice and prompts the next action.
    This function processes the user's language preference from the message text.
    If the input is not 'English' or 'Arabic', it prompts the user to select a valid language.
    Once a valid language is selected, it sets the user's language code in the context and
    sends a message asking the user to choose the next action.

    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object that contains user data.
    Returns:
        int: The next state of the conversation handler.
    """
    conversation: dict[str] = {
        'tasks': {
            'en': ''.join([
                '<b>Please choose what you want to do next:</b>\n\n'
                '1. Use analysis tools 🔍\n'
                '2. Generate a concept note 📄\n'
                '3. Generate full proposal 📑\n\n'
            ]),
            'ar': ''.join([
                '<b>الرجاء اختيار ما تريد القيام به:</b>\n\n'
                '1. استخدام أدوات التحليل 🔍\n'
                '2. إنشاء مذكرة مفاهيمية 📄\n'
                '3. إنشاء مقترح كامل 📑\n\n'
            ])
        },
        'error': {
            'en': '<b> Please select a valid language preference: either English or Arabic.</b>',
            'ar': '<b> الرجاء اختيار تفضيل لغة صالح: إما الإنجليزية أو العربية. </b>'
        }
    }

    if (update.message.text != 'English'
            and update.message.text != 'Arabic'):
        error: str = define_lang(
            (conversation['error'], update.effective_user.language_code)
        )
        await update.message.reply_text(
            error,
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
        logger.warning("Invalid language preference entered.")
        return USER_CHOICE_HANDLER

    if update.message.text == 'English':
        context.user_data['language_code'] = 'en'
    else:
        context.user_data['language_code'] = 'ar'

    logger.info(
        f"User selected language: {context.user_data['language_code']}")

    text: str = define_lang(
        conversation['tasks'], context.user_data['language_code'])

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(
            [[
                'Analysis Tools',
                'Generate Concept Note',
                'Generate Full Proposal'
            ]],
            one_time_keyboard=True,
            resize_keyboard=True
        ),
    )
    logger.info("Prompted user for next action based on language selection.")
    return CONVERSATION_HANDLER
