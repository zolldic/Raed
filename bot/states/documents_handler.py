#!/usr/bin/env python3
from telegram import Update, Document
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from logging import getLogger
from ..utils.utilties import define_lang, process_documents
from .. import SET_TASKS, SET_DOCUMENT

logger = getLogger(__name__)


async def handle_documents_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
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
            ]),
            'ar': ''.join([
                '<b>تم التحميل بنجاح ✅</b>\n\n',
                'تم تحميل المستند بنجاح!\n\n',
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
        return SET_TASKS
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
