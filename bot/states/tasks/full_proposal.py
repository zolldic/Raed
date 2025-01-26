#!/usr/bin/env python3

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from ...utils.gemini import generate_full_proposal

from ...utils.utilties import define_language


async def write_proposal_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input = update.message.text
    profile = context.user_data["profile"]

    response = generate_full_proposal(input, profile)
    await update.message.reply_text(
        f"""<b>Full Proposal:</b>
        {response}
        """,
        parse_mode='HTML'
    )
    html_text = define_language('end', context.user_data['language_code'])
    await update.message.reply_text(
        html_text,
        parse_mode='HTML'
    )
    return ConversationHandler.END
