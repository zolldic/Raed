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
import asyncio
import logging
import logging.handlers
from signal import SIGINT, SIGTERM
import os
import sys
from telegram.error import Conflict
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler, CallbackQueryHandler
)


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


async def main():
    """Main entry point for the bot application.
        This function initializes the bot application,
            sets up signal handlers for graceful shutdown,
            configures logging, and starts the bot either in
            polling mode (for development) or
            webhook mode (for production).
    """

    # create the bot application
    application: Application = ApplicationBuilder().token(BOT_KEY).build()

    # create conversation handler
    conversation: ConversationHandler = await create_states()

    # add the conversation handler to the bot application
    application.add_handler(conversation)

    # get the event loop
    event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    # signal handlers for shutdown in case of SIGINT or SIGTERM
    def signal_handler():
        event_loop.create_task(shutdown_application(application))

    # add signal handlers for SIGINT and SIGTERM
    for signal in (SIGINT, SIGTERM):
        event_loop.add_signal_handler(signal, signal_handler)

    # configure logging for the bot application
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.handlers.TimedRotatingFileHandler(
                filename='logs/bot.log',
                when='midnight',
                interval=1,
                backupCount=5,
                encoding='utf-8'
            ),
            # logging.StreamHandler() # for debugging
        ]
    )

    # set the log level for the httpx library to WARNING
    logging.getLogger('httpx').setLevel(logging.WARNING)

    # start the bot application in polling mode
    async with application:
        await application.start()
        try:
            await application.updater.start_polling()  # for development
        except Conflict as e:
            logging.error(f"Error starting the bot: {e}")
            sys.exit(1)

        # keep the event loop running
        while True:
            await asyncio.sleep(3600)

    # start the bot applicaiton in webhook mode
    # try:
    #    await application.initialize()
    #    await application.start()
        # await application.run_webhook(
        # listen='0.0.0.0',
        # port=8443,
        # url_path=f"https://127.0.0.1/{BOT_KEY}"
        # ) # for production
    # except Exception as e:
    #    await application.stop()
    #    await application.shutdown()


async def create_states():
    """Creates and returns a conversation handler for the bot application."""

    # create the conversation handler
    return ConversationHandler(
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


async def shutdown_application(app: Application,
                               event_loop: asyncio.AbstractEventLoop):
    """This function stops the bot application and closes the event loop.

        Args:
            application (ApplicationBuilder):
                The bot application to be stopped.
            event_loop (asyncio.AbstractEventLoop):
                The event loop to be closed.
    """

    # get the logger for the application
    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Shutting down the bot application...')

    # stop the updater and the bot
    await app.updater.stop()
    await app.stop()
    await app.shutdown()

    # fetch all running tasks in the event loop to cancel them
    tasks = [
        task for task in asyncio.all_tasks() if
        task is not asyncio.current_task()
    ]

    # cancel all tasks in the event loop
    [task.cancel() for task in tasks]

    # wait for all tasks to be cancelled
    await asyncio.gather(*tasks, return_exceptions=True)

    # close the event loop
    event_loop.stop()


if __name__ == '__main__':
    # create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # run the bot application
    asyncio.run(main(), debug=True)
