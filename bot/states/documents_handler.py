#!/usr/bin/env python3
"""This module handles the document upload process for a Telegram bot.

Functions:
    handle_documents_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Asynchronously handles the document upload process, processes the document,
        and sends a success or error message to the user based on the outcome.
"""
from telegram import Update, Document
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from logging import getLogger
from ..utils.utilties import define_lang, process_documents
from .. import CONCEPT_NOTE, SET_DOCUMENT

logger = getLogger(__name__)


async def handle_documents_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the document upload process in a conversation.

    This function processes the document uploaded by the user, checks its validity,
    and provides appropriate feedback messages in either English or Arabic based on
    the user's language preference. If the document is successfully processed, it
    stores the document content in the user's data and sends a success message.
    If an error occurs during the upload, it sends an error message and logs the error.

    Args:
        update (Update): The update object that contains the document uploaded by the user.
        context (ContextTypes.DEFAULT_TYPE): The context object that provides access to bot data and user data.

    Returns:
        int: The next state in the conversation flow.
    """

    conversation: dict[str, str] = {
        'upload_error': {
            'en': ''.join([
                '<b>Upload Failed ❌</b>\n\n',
                'The document could not be uploaded. Please ensure:\n',
                '- The file is in .docx or .pdf format.\n',
                '- The file size is within the allowed limit.\n\n',
                '<i>Please try again.</i>'
            ]),
            'ar': ''.join([
                '<b>فشل التحميل ❌</b>\n\n',
                'تعذر تحميل المستند. يرجى التأكد من:\n',
                '- أن الملف بصيغة .docx أو .pdf.\n',
                '- أن حجم الملف ضمن الحد المسموح.\n\n',
                '<i>الرجاء المحاولة مرة أخرى.</i>'
            ])
        },
        'upload_success': {
            'en': ''.join([
                '<b>Upload Successful ✅</b>\n\n',
                'Your document has been uploaded successfully!\n\n',
                'To proceed, please provide details about your project or the problem you want to address. ',
                'This will help us create a well-structured concept note for you.\n\n'
            ]),
            'ar': ''.join([
                '<b>تم التحميل بنجاح ✅</b>\n\n',
                'تم تحميل المستند بنجاح!\n\n',
                'للمتابعة، يرجى توضيح تفاصيل مشروعك أو المشكلة التي ترغب في معالجتها، ',
                'سيساعدنا ذلك في إنشاء مذكرة مفهوم منظمة جيدًا لك.\n\n'
            ])
        }

    }

    try:
        document: Document = update.message.document
        file = await context.bot.get_file(document.file_id)
        content = process_documents(file, document.file_name)
        context.user_data["document"] = content
        await update.message.reply_text(
            define_lang(
                conversation['upload_success'], context.user_data['language_code']
            ),
            parse_mode=ParseMode.HTML
        )
        return CONCEPT_NOTE
    except Exception as e:
        await update.message.reply_text(
            define_lang(
                conversation['upload_error'], context.user_data['language_code']
            ),
            parse_mode=ParseMode.HTML
        )
        logger.error(
            f"File upload error: {e}\n")
        return SET_DOCUMENT
