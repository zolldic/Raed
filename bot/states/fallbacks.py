#!/usr/bin/env python3
""" """ 
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
  ContextTypes,
  ConversationHandler
  
  )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text("GoodBye!", reply_markup=ReplyKeyboardRemove())
  return ConversationHandler.END