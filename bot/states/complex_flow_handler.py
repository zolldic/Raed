#!/usr/bin/env python3
"""
This module handles the complex flow of user interactions in a Telegram bot.

It defines the `flow_handler` function which processes user messages and directs
the flow of conversation based on the user's input. The function uses the
`telegram` library to interact with the Telegram API and the `logging` library
to log user actions.

Functions:
    flow_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Handles user messages and directs the flow of conversation based on the
        user's input. Returns the next state of the conversation.

Constants:
    FLOW_HANDLER: int
        The state representing the flow handler.
    CONCEPT_NOTE: int
        The state representing the generation of a concept note.
    FULL_PROPOSAL: int
        The state representing the generation of a full proposal.
"""

from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler)
from logging import getLogger
from .. import (
    FLOW_HANDLER, PESTEL_ANALYSIS,
    SWOT_ANALYSIS, CONCEPT_NOTE,
    FULL_PROPOSAL)

logger = getLogger(__name__)


async def flow_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the flow of conversation based on the user's message text.
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object for the conversation.
        Returns:
        int: The next state of the conversation based on the user's selection.
            - CONCEPT_NOTE: If the user selects 'Generate Concept Note'.
            - FULL_PROPOSAL: If the user selects 'Generate Full Proposal'.
            - PESTEL_ANALYSIS: If the user selects 'Generate PESTEL Analysis'.
            - SWOT_ANALYSIS: If the user selects 'Generate SWOT Analysis'.
            - ConversationHandler.END: If the user selects 'End Conversation'.
            - FLOW_HANDLER: If the user selects an invalid option.
    """

    match update.message.text:
        case 'Generate Concept Note':
            logger.info("User selected 'Generate Concept Note'")
            return CONCEPT_NOTE
        case 'Generate Full Proposal':
            logger.info("User selected 'Generate Full Proposal'")
            return FULL_PROPOSAL
        case 'Generate PESTEL Analysis':
            logger.info("User selected 'Generate PESTEL Analysis'")
            return PESTEL_ANALYSIS
        case 'Generate SWOT Analysis':
            logger.info("User selected 'Generate SWOT Analysis'")
            return SWOT_ANALYSIS
        case 'End Conversation':
            logger.info("User selected 'End Conversation'")
            return ConversationHandler.END
        case _:
            await update.message.reply_text(
                "Please select a valid option",
                parse_mode='HTML'
            )
            return FLOW_HANDLER
