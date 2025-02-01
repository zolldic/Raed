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
from . import (USER_CHOICE_HANDLER, CONVERSATION_HANDLER,
               ANALYSIS_TOOLS, PROBLEM_TREE_ANALYSIS,
               SWOT_ANALYSIS, PESTEL_ANALYSIS,
               CONCEPT_NOTE, FULL_PROPOSAL,
               FLOW_HANDLER)

from .states.start_conversation import start
from .states.user_choice_handler import user_choice
from .states.tasks_handler import tasks
from .states.complex_flow_handler import flow_handler

# analysis tools
from .states.analysis_tools import choose_analysis_method
from .states.tasks.problem_tree_analysis import problem_tree_method
from .states.tasks.swot_analysis import swot_analysis_method
from .states.tasks.pestel_analysis import pestel_analysis_method
from .states.tasks.concept_note import handle_concept_note
from .states.tasks.full_proposal import handle_full_roposal
# fallback
from .states.fallbacks import cancel


def main():
    """
    """

    application = ApplicationBuilder().token(BOT_KEY).build()
    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            USER_CHOICE_HANDLER: [MessageHandler(
                filters.TEXT & (~filters.COMMAND), user_choice
            )],
            CONVERSATION_HANDLER: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                tasks
            )],
            ANALYSIS_TOOLS: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                choose_analysis_method
            )],
            PROBLEM_TREE_ANALYSIS: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                problem_tree_method
            )],
            SWOT_ANALYSIS: [MessageHandler(
                filters.TEXT & filters.Document.ALL & (~filters.COMMAND),
                swot_analysis_method
            )],
            PESTEL_ANALYSIS: [MessageHandler(
                filters.TEXT & filters.Document.ALL & (~filters.COMMAND),
                pestel_analysis_method
            )],
            CONCEPT_NOTE: [MessageHandler(
                filters.TEXT & filters.Document.ALL & (~filters.COMMAND),
                handle_concept_note
            )],
            FULL_PROPOSAL: [MessageHandler(
                filters.TEXT & filters.Document.ALL & (~filters.COMMAND),
                handle_concept_note
            )],
            FLOW_HANDLER: [MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                flow_handler
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
