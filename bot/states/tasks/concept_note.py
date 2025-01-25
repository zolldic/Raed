#!/usr/bin/env python3

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from ...utils.gemini import generate_concept_note
async def create_note_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = update.message.text
    profile = context.user_data["profile"]
    
    response = generate_concept_note(input, profile)
    await update.message.reply_text(
        f"""<b>Concept note:</b>
        {response}
        """,
        parse_mode='HTML'
        )
    await update.message.reply_text(
        """ type /start to restart the bot""",
        parse_mode='HTML'
        )
    return ConversationHandler.END