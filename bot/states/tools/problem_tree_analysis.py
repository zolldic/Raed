#!/usr/bin/env python3
"""This module contains the implementation of the problem tree analysis method for a Telegram bot.

Functions:
    problem_tree_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Handles the problem tree analysis by receiving user input, performing analysis, and providing options for further actions.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from logging import getLogger

from ...gemini.base import Model
from ...utils.utilties import define_lang
from ... import SET_TASKS, PROBLEM_TREE_ANALYSIS

logger = getLogger(__name__)


async def problem_tree_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the problem tree analysis process.
    This method extracts the user's problem statement from the update message,
    performs a problem tree analysis using the analysis model, and stores the
    analysis result in the user's context data. It then prompts the user with
    options to generate a concept note, a full proposal, or end the conversation.
    Args:
        update (Update): The update object containing the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for storing user data.
    Returns:
        int: The next state in the conversation flow.
    """
    conversation: dict[str, str] = {
        'success': {
            'en': ''.join([
                '<b>Based on the analysis provided:</b>\n\n',
                '1. Generate a concept note 📄\n',
                '2. Generate a full proposal 📑\n',
                '3. End the conversation 👋\n\n',
            ]),
            'ar': ''.join([
                '<b>بناءً على التحليل المقدم:</b>\n\n',
                '1. إنشاء مذكرة مفاهيمية 📄\n',
                '2. إنشاء مقترح كامل 📑\n',
                '3. إنهاء المحادثة 👋\n\n',

            ]),
        },
        'error': {
            'en': 'Please try again. ❌',
            'ar': 'يرجى المحاولة مرة أخرى ❌'
        }
    }

    try:
        response: str = Model.problem_tree_analysis(
            update.message.text)
        context.user_data['tree_analysis'] = response
        await update.message.reply_text(
            response,
            parse_mode=ParseMode.HTML
        )

        success: str = define_lang(conversation['success'],
                                   context.user_data['language_code'])
        await update.message.reply_text(
            success,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('Generate A Concept Note', callback_data='CONCEPT_NOTE')
                 ],
                [InlineKeyboardButton('Generate A Proposal', callback_data='FULL_PROPOSAL')
                 ],
                [InlineKeyboardButton('End the Conversation', callback_data='END')
                 ],
            ]),
        )
        logger.info("Problem tree analysis completed successfully.")
        return SET_TASKS
    except Exception as e:
        logger.error(f"Error: {e}")
        return PROBLEM_TREE_ANALYSIS
