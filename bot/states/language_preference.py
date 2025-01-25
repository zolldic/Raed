#!/usr/bin/env pythono3

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils.utilties import define_language

from .. import CHOICE, SET_LANGUAGE


async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    if (update.message.text != 'English'
            and update.message.text != 'Arabic'):
        await update.message.reply_text(
            f'<b> You entered {update.message.text}. Please select a valid language preference: either English or Arabic.</b>',
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(

                [[
                    'English',
                    'Arabic'
                ]],
                one_time_keyboard=True,
                resize_keyboard=True
            ),

        )
        return SET_LANGUAGE

    context.user_data['language_code'] = update.message.text
    html_text: str = define_language(
        'user_type', context.user_data['language_code'])
    await update.message.reply_text(
        html_text,
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(
            [
                [
                    'Activist',
                    'Organization'
                ]
            ],
            one_time_keyboard=True,
            resize_keyboard=True
        ),

    )
    return CHOICE
