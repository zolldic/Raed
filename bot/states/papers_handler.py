#!/usr/bin/env python3
"""
This module contains the task for creating a concept note using the Telegram bot.

Functions:
    async def generate_papers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Handles the generation of papers based on user interaction.
"""

from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from logging import getLogger
from ..utils.utilties import define_lang
from .. import SET_DOCUMENT, CONCEPT_NOTE


logger = getLogger(__name__)


async def generate_papers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the generation of papers based on user interaction.

    This function processes the user's callback query to either prompt them to upload a document
    or describe a problem for generating a concept note. The response is based on the user's
    selection and their current context.

    Args:
        update(Update): The update object that contains the callback query.
        context(ContextTypes.DEFAULT_TYPE): The context object that holds user data and other
                                             contextual information.

    Returns:
        int: The next state in the conversation flow, either SET_DOCUMENT or CONCEPT_NOTE.
    """

    conversation: dict[str, str] = {
        'Yes': {
            'en': ''.join([
                '<b>Upload Document 📂</b>\n\n',
                'Please upload your document (organization profile, project details, etc.).\n\n',
                '<b>Allowed formats:</b> .docx, .pdf\n\n',
                '<i>Click the attachment icon or drag and drop your file.</i>'
            ]),
            'ar': ''.join([
                '<b>تحميل المستند 📂</b>\n\n',
                'الرجاء تحميل المستند الخاص بك (ملف تعريف المنظمة، تفاصيل المشروع، إلخ).\n\n',
                '<b>الصيغ المسموحة:</b> .docx, .pdf\n\n',
                '<i>انقر على أيقونة المرفق أو قم بسحب وإفلات الملف.</i>'
            ])
        },
        'concept_note': {
            'en': ''.join([
                '<b>Concept Note Generation 📄</b>\n\n',
                'A concept note is a concise document summarizing a project\'s purpose, objectives, and expected impact.\n\n',
                '<b>Please describe the problem you want to address:</b>\n',
                '<i>Example: "Lack of access to clean water in rural communities."</i>\n\n',
                '<i>Type your response below.</i>'
            ]),
            'ar': ''.join([
                '<b>إنشاء مذكرة مفاهيمية 📄</b>\n\n',
                'المذكرة المفاهيمية هي وثيقة موجزة تُلخص الغرض، الأهداف، والأثر المتوقع للمشروع.\n\n',
                '<b>الرجاء وصف المشكلة التي ترغب في معالجتها:</b>\n',
                '<i>مثال: "نقص الوصول إلى المياه النظيفة في المجتمعات الريفية."</i>\n\n',
                '<i>اكتب ردك أدناه.</i>'
            ])
        }
    }

    query: CallbackQuery = update.callback_query
    await query.answer()

    if (query.data == 'Yes' and
            context.user_data.get("document") == None):
        await query.edit_message_text(
            text=define_lang(conversation['Yes'],
                             context.user_data['language_code']),
            parse_mode=ParseMode.HTML
        )
        logger.info("Prompting user to upload a document.")
        return SET_DOCUMENT

    else:
        await query.edit_message_text(
            text=define_lang(conversation['concept_note'],
                             context.user_data['language_code']),
            parse_mode=ParseMode.HTML
        )
        logger.info(
            "Prompting user to describe the problem for the concept note.")
        return CONCEPT_NOTE
