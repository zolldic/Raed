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
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

from .config import BOT_KEY
from . import SET_LANGUAGE, CHOICE, UPLOAD_PROFILE, CHOOSE_TASK, ANALYZE_PROBLEM, CREATE_NOTE, WRITE_PROPOSAL

from .states.start_conversation import start
from .states.language_preference import set_language
from .states.user_type import user_choice
from .states.upload_file import prfile_upload
from .states.tasks_handler import choose_task
from .states.fallbacks import cancel

from .states.tasks.analyze_problem import analyze_problem_task
from .states.tasks.concept_note import create_note_task
from .states.tasks.full_proposal import write_proposal_task


def main():
    """Initializes and runs the Telegram bot application.
        Steps:
            1. Build the bot application using the ApplicationBuilder
                with the bot token.
            2. Define a ConversationHandler to manage
                the bot's conversation flow:
                - Entry point: /start command.
                - States:
                - CHOICE: Captures the user's role or task choice.
                    - Fallback: /cancel command to exit the conversation.
            3. Add the conversation handler to the bot's application.
            4. Start polling for updates and handle user messages
                in real-time.
    """

    application = ApplicationBuilder().token(BOT_KEY).build()
    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SET_LANGUAGE: [MessageHandler(
                filters.TEXT & (~filters.COMMAND), set_language
            )],
            CHOICE: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                user_choice
            )],
            UPLOAD_PROFILE: [MessageHandler(
                filters.Document.ALL,
                prfile_upload
            )],
            CHOOSE_TASK: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                choose_task
            )],
            ANALYZE_PROBLEM: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                analyze_problem_task
            )],
            CREATE_NOTE: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                create_note_task
            )],
            WRITE_PROPOSAL: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                write_proposal_task
            )],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conversation)
    application.run_polling()


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('logs/bot.log'),
            logging.StreamHandler()
        ]
    )

    main()
