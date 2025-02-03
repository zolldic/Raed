#!/usr/bin/env python3
"""This module handles the language selection for the bot.

    Functions:
        set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Asynchronously sets the language for the user based on their selection
        and updates the conversation state.
"""

from telegram import (
    Update, InlineKeyboardButton,
    InlineKeyboardMarkup, CallbackQuery
)
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from logging import getLogger

from .. import SET_TASKS
from ..utils.utilties import define_lang

logger = getLogger(__name__)


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the setting of the user's language preference based on their callback query.

    Args:
        update (Update): The update object that contains the callback query.
        context (ContextTypes.DEFAULT_TYPE): The context object that contains user data and bot information.

    Returns:
        int: The next state of the conversation handler.
    """

    query: CallbackQuery = update.callback_query
    await query.answer()
    lang: str = query.data

    context.user_data.update(
        {'language_code': lang}
    )

    conversation: dict = {
        'query': {
            'en': f'Your language has been set to {lang}. 🌐',
            'ar': f'تم تعيين اللغة إلى {lang}. 🌐'
        },
        'message': {
            'en': ''.join([
                '<b>What would you like to do next?</b>\n\n',
                '1. Use analysis tools 🔍\n',
                '2. Generate a concept note 📄\n',
            ]),
            'ar': ''.join([
                '<b>ماذا تريد أن تفعل بعد ذلك؟</b>\n\n',
                '1. استخدام أدوات التحليل 🔍\n',
                '2. إنشاء مذكرة مفاهيمية 📄\n',
            ])
        }
    }

    await query.edit_message_text(
        define_lang(conversation['query'], lang),
        parse_mode=ParseMode.HTML)

    # next State
    message: str = define_lang(conversation['message'], lang)
    await context.bot.send_message(
        text=message, chat_id=context._chat_id,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    'Use Analysis Tools', callback_data='ANALYSIS_TOOLS')],
                [InlineKeyboardButton(
                    'Generate A Concept Note', callback_data='CONCEPT_NOTE')],
            ]
        ),
        parse_mode=ParseMode.HTML
    )

    logger.info(
        f"User {update.effective_user.id} set their language to {lang}")
    return SET_TASKS
