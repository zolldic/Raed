#!/usr/bin/env python3
"""Telegram Bot Application for Activist Support
    This script initializes and runs a Telegram bot designed
    to assist activists, organizations, and changemakers
    in crafting impactful documents, analyzing problems,
    and simplifying the process of proposal writing.
    The bot uses a conversation-based flow to guide
    users through various tasks.

    Functions:
        main(): Initializes the bot application, sets up handlers,
        and starts polling for messages.
"""
import logging
import logging.handlers
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler, CallbackQueryHandler
)

import os
from .config import BOT_KEY
from . import (SET_LANGUAGE, SET_TASKS,
               ANALYSIS_TOOLS, PROBLEM_TREE_ANALYSIS,
               SWOT_ANALYSIS, PESTEL_ANALYSIS,
               CONCEPT_NOTE, SET_PAPER, SET_DOCUMENT
               )

from .states.entry_point import start
from .states.language_handler import set_language
from .states.tasks_handler import set_tasks
from .states.analysis_tools import set_analysis_method
from .states.tools.problem_tree_analysis import problem_tree_method
from .states.tools.swot_analysis import swot_analysis_method
from .states.tools.pestel_analysis import pestel_analysis_method

from .states.papers_handler import generate_papers
from .states.papers.concept_note_handler import concept_note
from .states.documents_handler import handle_documents_upload

from .states.fallbacks import cancel


def main():
    """Initializes and runs the bot application.
    This function sets up the bot application using the ApplicationBuilder with the provided BOT_KEY.
    It defines a ConversationHandler with various states and corresponding handlers for different
    user interactions.
    """

    application = ApplicationBuilder().token(BOT_KEY).build()
    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SET_LANGUAGE: [CallbackQueryHandler(set_language)],
            SET_TASKS: [CallbackQueryHandler(set_tasks)],
            ANALYSIS_TOOLS: [CallbackQueryHandler(set_analysis_method)],
            PROBLEM_TREE_ANALYSIS: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                problem_tree_method
            )],
            SWOT_ANALYSIS: [MessageHandler(
                            filters.TEXT & (~filters.COMMAND),
                            swot_analysis_method
                            )],
            PESTEL_ANALYSIS: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                pestel_analysis_method
            )],
            SET_PAPER: [CallbackQueryHandler(
                generate_papers
            )],
            CONCEPT_NOTE: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                concept_note
            )],
            SET_DOCUMENT: [MessageHandler(
                filters.Document.ALL & (~filters.COMMAND),
                handle_documents_upload
            )],
            # END: [CallbackQueryHandler(end_conversation)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conversation)
    application.run_polling()


if __name__ == '__main__':
    os.makedirs('logs', exist_ok=True)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # file handler for logs.
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename='logs/bot.log',
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # stream (console) handler for logs.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            file_handler  # , console_handler # for test purposes
        ]
    )
    # reduce httpx
    logging.getLogger('httpx').setLevel(logging.WARNING)
    main()
