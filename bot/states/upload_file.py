#!/usr/bin/env python3
"""Module for handling profile uploads
    in the Telegram bot.
"""
from telegram import (
    Update,
    Document,
    ReplyKeyboardMarkup)
from telegram.ext import ContextTypes
from io import BytesIO
import logging
from ..utils.utilties import (
    define_lang,
    verify_file_format,
    extract_text_from_file)

from .. import UPLOAD_PROFILE, CHOOSE_TASK

logger = logging.getLogger(__name__)


async def prfile_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the upload of an organization's
        profile document and validates its format.

        Args:
            update (telegram.Update): Incoming update object that contains the user's message and metadata.
            context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context object containing user-specific data.

        Returns:
            int: The next conversation state (CHOOSE_TASK or UPLOAD_PROFILE).
    """

    conversation: dict[str] = {
        'success': {
            'en': "Profile uploaded successfully! Now, choose what you'd like to do:",

            'ar': "تم تحميل الملف الشخصي بنجاح! الآن، اختر ما تريد القيام به:"
        },
        'error': {
            'en': "Please upload a valid profile document. Accepted file types are PDF, DOCX or DOC.",
            'ar': "يرجى تحميل ملف تعريف صالح. أنواع الملفات المقبولة هي PDF, DOCX or DOC."
        }}

    text: str = ''

    if not update.message.document:
        text = define_lang(
            conversation['error'], context.user_data['language_code']
        )
        await update.message.reply_text(
            text,
            parse_mode='HTML')
        logger.warning(
            "No document uploaded by the user. Returning to UPLOAD_PROFILE state.")
        return UPLOAD_PROFILE

    document: Document = update.message.document
    # check if document is bigger then 15MB ?

    if not verify_file_format(document.file_name):
        text = define_lang(
            conversation['error'], context.user_data['language_code']
        )
        await update.message.reply_text(
            text,
            parse_mode='HTML'
        )
        logger.warning(
            f"Invalid file format uploaded by user: {document.file_name}.")
        return UPLOAD_PROFILE
    try:
        file = await context.bot.get_file(document.file_id)
        file_byte = await file.download_as_bytearray()
        buffer = BytesIO(file_byte)

        pdf_text = extract_text_from_file(buffer, document.file_name)

        context.user_data["Org_profile"] = pdf_text

        text = define_lang(
            conversation['success'], context.user_data['language_code']
        )

        await update.message.reply_text(
            text,
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        'Analyze a problem',
                        'Create a concept note',
                        'Write a full proposal'
                    ]
                ],
                one_time_keyboard=True,
                resize_keyboard=True
            ),
        )
        logger.info(
            f"Profile uploaded successfully by user. File saved at: {file_path}. Proceeding to CHOOSE_TASK state."
        )
        return CHOOSE_TASK
    except Exception as e:
        logging.error(f"File upload error: {e}\n return to UPLOAD PROFILE")
        text = define_lang(
            conversation['error'], context.user_data['language_code']
        )
        await update.message.reply_text(
            text,
            parse_mode='HTML'
        )
        return UPLOAD_PROFILE
