#!/usr/bin/env python3
"""This module provides functionality for handling SWOT analysis using Telegram bot.

    Functions:
        swot_analysis_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
            Handles the SWOT analysis process.
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from logging import getLogger
from ...gemini.base import Model
from ...utils.utilties import define_lang

from ... import SWOT_ANALYSIS

logger = getLogger(__name__)


async def swot_analysis_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the SWOT analysis process for the user.

    Args:
        update (Update): The update object that contains information about the incoming update.
        context (ContextTypes.DEFAULT_TYPE): The context object that contains user data and other context-specific information.
    Returns:
        int: The next state of the conversation flow.
    """

    conversation: dict[str, str] = {
        'success': {
            'en': 'Thank you for using Raed. Have a great day! 👋',
            'ar': 'شكرًا لاستخدام رائد. أتمنى لك يومًا سعيدًا! 👋'
        },
        'error': {
            'en': 'Please try again. ❌',
            'ar': 'يرجى المحاولة مرة أخرى ❌'
        }
    }

    try:
        response: str = Model.swot_analysis(update.message.text)
        context.user_data['swot_analysis'] = response

        await update.message.reply_text(
            response,
            parse_mode='HTML'
        )
        await update.message.reply_text(
            define_lang(conversation['success'],
                        context.user_data['language_code']),
            parse_mode='HTML'
        )
        logger.info("SWOT analysis completed and response sent to user.")

        return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text(
            define_lang(
                conversation['error'], context.user_data['language_code']
            ),
            parse_mode='HTML'
        )

        logger.error(f"Error: {e}\n return to SWOT Analysis")
        return SWOT_ANALYSIS
