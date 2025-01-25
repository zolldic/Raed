#!/usr/bin/env python3
"""
Module for handling task selection in the Telegram bot.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

from .. import CHOOSE_TASK, ANALYZE_PROBLEM, CREATE_NOTE, WRITE_PROPOSAL


from ..utils.utilties import define_language

logger = logging.getLogger(__name__)


async def choose_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the user's task selection and transitions
        to the appropriate state based on their choice

        Args:
            update (telegram.Update): Incoming update object containing the user's message and metadata.
            context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context object for storing user-specific data.

        Returns:
            int: The next conversation state (
                ANALYZE_PROBLEM,
                CREATE_NOTE,
                WRITE_PROPOSAL or CHOOSE_TASK
                ).
    """

    task = update.message.text
    context.user_data['task'] = task

    if task == "Analyze a problem":
        html_text: str = define_language(
            'analyze_problem', context.user_data['langauge_code'])
        await update.message.reply_text(
            html_text,
            parse_mode='HTML'
        )

        logger.info(
            "User selected 'Analyze a problem'. Transitioning to ANALYZE_PROBLEM state.")
        return ANALYZE_PROBLEM

    elif task == "Create a concept note":
        html_text = define_language(
            'concept_note', context.user_data['langauge_code'])
        await update.message.reply_text(
            html_text,
            parse_mode='HTML'
        )
        logger.info(
            "User selected 'Create a concept note'. Transitioning to CREATE_NOTE state.")
        return CREATE_NOTE
    elif task == "Write a full proposal":
        html_text: str = define_language(
            'full_proposal', context.user_data['langauge_code'])
        await update.message.reply_text(
            html_text,
            parse_mode='HTML'
        )

        logger.info(
            "User selected 'Write a full proposal'. Transitioning to WRITE_PROPOSAL state.")
        return WRITE_PROPOSAL
    else:
        html_text: str = define_language(
            'invalid_choice', context.user_data['language_code'])
        await update.message.reply_text(
            html_text,
            parse_mode='HTML'
        )
        logger.warning(
            f"User provided an invalid choice: {task}. Returning to CHOOSE_TASK state.")
        return CHOOSE_TASK
