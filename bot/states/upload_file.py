#!/usr/bin/env python3
"""Module for handling profile uploads
    in the Telegram bot.
"""
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import os
import logging

from .. import UPLOAD_PROFILE, CHOOSE_TASK
from ..utils.utilties import define_language, extract_text

logger = logging.getLogger(__name__)


async def prfile_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the upload of an organization's
        profile document and validates its format.

        Args:
            update (telegram.Update): Incoming update object that contains the user's message and metadata.
            context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context object containing user-specific data.

        Returns:
            int: The next conversation state (CHOOSE_TASK or UPLOAD_PROFILE).
    """

    allowed_ext = {'pdf'}
    file = update.message.document

    if not file:
        html_text: str = define_language(
            'error_valid_document', context.user_data['language_code']
        )
        await update.message.reply_text(
            html_text,
            parse_mode='HTML')
        logger.warning(
            "No document uploaded by the user. Returning to UPLOAD_PROFILE state.")
        return UPLOAD_PROFILE

    file_name = file.file_name
    if not any(file_name.endswith(ext) for ext in allowed_ext):
        html_text: str = define_language(
            'error_valid_document', context.user_data['language_code']
        )
        await update.message.reply_text(
            html_text,
            parse_mode='HTML'
        )
        logger.warning(
            f"Invalid file format uploaded by user: {file_name}. Expected formats: {', '.join(allowed_ext)}.")
        return UPLOAD_PROFILE

    try:
        directory = "org_profiles"

        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            logger.info(f"Created directory for profile uploads: {directory}")

        file_info = await context.bot.get_file(file.file_id)
        file_path = os.path.join(directory, file_name)

        await file_info.download_to_drive(file_path)
        context.user_data["org_profile"] = file_path
        context.user_data["profile"] = extract_text(file_path)

        html_text: str = define_language(
            'upload_success', context.user_data['language_code']
        )
        await update.message.reply_text(
            html_text,
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
        html_text: str = define_language(
            'error_valid_document', context.user_data['language_code']
        )
        await update.message.reply_text(
            html_text,
            parse_mode='HTML'
        )
        return UPLOAD_PROFILE
