#!/usr/bin/env python3
"""
This module handles the generation of concept notes using the Telegram bot framework.

Functions:
    concept_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        Asynchronously generates a concept note based on user input and replies with the generated note.
        Handles errors by sending an appropriate error message to the user.
"""

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from logging import getLogger

from ...utils.utilties import define_lang
from ...gemini.base import Model
from ... import CONCEPT_NOTE

logger = getLogger(__name__)


async def concept_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Handle the concept note generation process for the user.

    This function receives an update and context, processes the user's input to generate a concept note,
    and sends the generated note back to the user. If an error occurs during the generation process,
    an error message is sent to the user.

    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.

    Returns:
        str: The state of the conversation. Returns ConversationHandler.END if the process is successful,
             otherwise returns CONCEPT_NOTE to indicate an error occurred.
    """

    conversation: dict[str, str] = {
        'error': {

            'en': ''.join([
                '<b>Error Generating Concept Note ❌</b>\n\n',
                'We encountered an issue while generating your concept note.\n\n',
                'Please check your input and try again. If the problem persists, ensure that all necessary details are provided or contact support for assistance.\n\n'
            ]),
            'ar': ''.join([
                '<b>خطأ في إنشاء مذكرة المفهوم ❌</b>\n\n',
                'حدثت مشكلة أثناء إنشاء مذكرة المفهوم الخاصة بك.\n\n',
                'يرجى التحقق من المدخلات والمحاولة مرة أخرى. إذا استمرت المشكلة، تأكد من تقديم جميع التفاصيل الضرورية أو تواصل مع الدعم للمساعدة.\n\n'
            ])
        },
        'END': {
            'en': 'Thank you for using Raed. Have a great day! 👋',
            'ar': 'شكرًا لاستخدام رائد. أتمنى لك يومًا سعيدًا! 👋'

        }
    }
    text: str = update.message.text

    try:
        profile: str = context.user_data.get("document")
        response: str = Model.generate_concept_note(
            text, profile)
        await update.message.reply_text(
            response,
            parse_mode=ParseMode.HTML
        )
        await update.message.reply_text(
            define_lang(conversation['END'],
                        context.user_data['language_code']),
            parse_mode=ParseMode.HTML
        )
        logger.info(
            f"Concept note generated successfully for user {update.effective_user.id}")
        return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text(
            define_lang(conversation['error'],
                        context.user_data['language_code']),
            parse_mode=ParseMode.HTML
        )
        logger.error(f"Error generating concept note: {e}")
        return CONCEPT_NOTE
