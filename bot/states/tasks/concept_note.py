#!/usr/bin/env python3
"""
This module contains the task for creating a concept note using the Telegram bot.

Functions:
    handle_concept_note(update: Update, context: ContextTypes.DEFAULT_TYPE)
        Asynchronously handles the creation of a concept note based on user input and profile data.
"""


from telegram import Update, Document
from telegram.ext import ContextTypes, ConversationHandler
from logging import getLogger

from ...gemini.base import Model
from ...utils.utilties import extract_text_from_file, define_lang, verify_file_format
from ... import CONCEPT_NOTE

from io import BytesIO
logger = getLogger(__name__)


async def handle_concept_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    """

    conversation: dict[str, str] = {
        'upload_document': {
            'en': ''.join([
                '<b>📤 Upload Your Organization Profile for Analysis</b>\n\n',
                'To provide a thorough understanding of your organization, please upload your organization profile. ',
                'This profile will help in evaluating the organization’s structure, mission, and key functions.\n\n',
                '<i>Accepted formats: PDF, DOCX, or DOC. Please upload your organization profile now.</i>'
            ]),
            'ar': ''.join([
                '<b>📤 تحميل ملف تعريف منظمتك للتحليل</b>\n\n',
                'لتوفير فهم شامل لمنظمتك، يرجى تحميل ملف تعريف منظمتك. ',
                'سيساعد هذا الملف في تقييم هيكل المنظمة، رسالتها، والوظائف الرئيسية.\n\n',
                '<i>الصيغ المقبولة: PDF، DOCX، أو DOC. يرجى تحميل ملف تعريف منظمتك الآن.</i>'
            ])
        },
        'upload_error': {
            'en': ''.join([
                '⚠️ <b>Error Uploading Document</b>\n\n',
                'There was an issue processing your document. Please ensure that:\n',
                '✔️ The file format is PDF, DOCX, or DOC.\n',
                '✔️ The document is not empty or corrupted.\n\n',
                '🔄 <b>Please try uploading the document again.</b>'
            ]),
            'ar': ''.join([
                '⚠️ <b>خطأ في تحميل المستند</b>\n\n',
                'حدثت مشكلة أثناء معالجة المستند. يرجى التأكد من:\n',
                '✔️ أن يكون الملف بصيغة PDF أو DOCX أو DOC.\n',
                '✔️ أن المستند ليس فارغًا أو تالفًا.\n\n',
                '🔄 <b>يرجى محاولة تحميل المستند مرة أخرى.</b>'
            ])
        }
    }

    if context.user_data["profile"]:
        text: str = update.message.text
        response = Model.generate_concept_note(
            text, context.user_data["profile"])
        await update.message.reply_text(
            response,
            parse_mode='HTML',
        )
        logger.info("concept note generated for user")
        return ConversationHandler.END

    context.bot.send_message(define_lang(
        conversation['upload_document']), parse_mode='HTML')

    document: Document = update.message.document

    if document:
        if not verify_file_format(document.file_name):
            error: str = define_lang(
                conversation['upload_error'], context.user_data['language_code']
            )
            await update.message.reply_text(
                error,
                parse_mode='HTML'
            )
            logger.warning(
                f"Invalid file format uploaded by user: {document.file_name}.")
            return CONCEPT_NOTE

        try:
            file = await context.bot.get_file(document.file_id)
            file_byte = await file.download_as_bytearray()
            buffer = BytesIO(file_byte)
            extracted_text = extract_text_from_file(buffer, document.file_name)

            context.user_data["profile"] = extracted_text
            response: str = Model.swot_analysis(extracted_text)
            context.user_data['concept_note'] = response

            await update.message.reply_text(
                response,
                parse_mode='HTML',
            )
            logger.info("concept note generated for user")
            return ConversationHandler.END
        except Exception as e:
            await update.message.reply_text(
                define_lang(
                    conversation['upload_error'], context.user_data['language_code']
                ),
                parse_mode='HTML'
            )
            logger.error(f"File upload error: {e}\n return to Concept Note")
            return CONCEPT_NOTE
