#!/usr/bin/env python3
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from ...utils.gemini import analyze_problem
from ...utils.utilties import define_language


async def analyze_problem_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    input = update.message.text
    context.user_data["problem"] = input
    response = analyze_problem(input)
    await update.message.reply_text(
        f"""<b>Problem Analysis</b>
        {response}
        """,
        parse_mode='HTML'
    )
    html_text = define_language('end', context.user_data['langauge_code'])
    await update.message.reply_text(
        html_text,
        parse_mode='HTML'
    )
    return ConversationHandler.END
