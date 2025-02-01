#!/usr/bin/env python3
"""This module provides functionality for handling PESTEL analysis using Telegram bot.

    Functions:
        pestel_analysis_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
            Handles the PESTEL analysis process. It verifies the uploaded document, extracts text from it,
            performs PESTEL analysis, and sends the analysis result back to the user.
"""
from telegram import (
    Update, Document,
    File, ReplyKeyboardMarkup
)
from telegram.ext import ContextTypes
from logging import getLogger
from ...gemini.base import Model
from ...utils.utilties import (
    verify_file_format, define_lang, process_documents
)
from ... import PESTEL_ANALYSIS, FLOW_HANDLER

logger = getLogger(__name__)


async def pestel_analysis_method(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the PESTEL analysis process for the user.
       This method processes the user's uploaded document, performs a PESTEL analysis,
       and responds with the analysis results. It also provides options for further actions.

       Args:
           update (Update): The update object that contains information about the incoming update.
           context (ContextTypes.DEFAULT_TYPE): The context object that contains user data and other context-specific information.
       Returns:
           int: The next state of the conversation flow.
       """
    conversation: dict[str, str] = {
        'upload_document': {
            'en': ''.join([
                '<b>📤 Upload Your Document for PESTEL Analysis</b>\n\n',
                'To provide a detailed analysis, please upload a document containing relevant information ',
                'about your organization, campaign, or project. This will help in evaluating:\n\n',
                '✅ <b>PESTEL Analysis:</b> Political, Economic, Social, Technological, Environmental, and Legal factors.\n\n',
                '<i>Accepted formats: PDF, DOCX, or DOC. Please upload your document now.</i>'
            ]),
            'ar': ''.join([
                '<b>📤 تحميل المستند لتحليل PESTEL</b>\n\n',
                'لإجراء تحليل مفصل، يرجى تحميل مستند يحتوي على معلومات ذات صلة ',
                'بمنظمتك أو حملتك أو مشروعك. سيساعد ذلك في تقييم:\n\n',
                '✅ <b>تحليل بيستل (PESTEL):</b> العوامل السياسية والاقتصادية والاجتماعية والتكنولوجية والبيئية والقانونية.\n\n',
                '<i>الصيغ المقبولة: PDF، DOCX، أو DOC. يرجى تحميل المستند الآن.</i>'
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

    if context.user_data.get('document'):
        response: str = Model.pestel_analysis(
            context.user_data.get('document'))
        context.user_data['pestel_analysis'] = response

        await update.message.reply_text(
            response,
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(
                [[
                    'Generate SWOT Analysis',
                    'End Conversation',
                ]],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
        logger.info("PESTEL analysis completed and response sent to user.")
        return FLOW_HANDLER

    context.bot.send_message(define_lang(
        conversation['upload_document']), parse_mode='HTML')

    document: Document = update.message.document

    if document:
        if not verify_file_format(document.file_name):
            error: str = define_lang(
                conversation['error_upload'], context.user_data['language_code']
            )
            await update.message.reply_text(
                error,
                parse_mode='HTML'
            )
            logger.warning(
                f"Invalid file format uploaded by user: {document.file_name}.")
            return PESTEL_ANALYSIS

        try:
            file: File = await context.bot.get_file(document.file_id)
            extracted_text = process_documents(file, document.file_name)
            context.user_data["document"] = extracted_text
            response: str = Model.pestel_analysis(extracted_text)
            context.user_data['pestel_analysis'] = response
            await update.message.reply_text(
                response,
                parse_mode='HTML',
                reply_markup=ReplyKeyboardMarkup(
                    [[
                        'Generate SWOT Analysis',
                        'End Conversation',

                    ]],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
            )
            logger.info(
                "PESTEL analysis completed and response sent to user.")
            return FLOW_HANDLER
        except Exception as e:
            text = define_lang(
                conversation['error_upload'], context.user_data['language_code']
            )
            await update.message.reply_text(
                text,
                parse_mode='HTML'
            )

            logger.error(
                f"File upload error: {e}\n return to PESTEL Analysis")
            return PESTEL_ANALYSIS
