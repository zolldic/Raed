#!/usr/bin/env python3
"""This module contains the start_conversation state for the Raed bot.

Functions:
    start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Initiates a conversation with the user, presenting a welcome message and language selection options.
"""
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    User
)
from telegram.ext import ContextTypes
from logging import getLogger

from .. import USER_CHOICE_HANDLER
from ..utils.utilties import define_lang

logger = getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ Initiates a conversation with the user and prompts them to select their preferred language.
    This function sends a welcome message to the user, providing information about the bot's purpose and available commands.
    It then asks the user to confirm their preferred language (English or Arabic) and sets up a reply keyboard for language selection.
    Args:
        update (Update): An object that contains all the information and data that the update event carries.
        context (ContextTypes.DEFAULT_TYPE): An object that contains the context for the conversation, including user data.
    Returns:
        int: The next state in the conversation, which is SET_LANGUAGE.
    """

    conversation: dict[str] = {
        'en': ''.join((
            "<b>Welcome to Raed, the Activist Support Bot!</b>\n",
            "Raed is designed to assist CSOs, activists, and changemakers in crafting impactful concept notes, full proposals, and analyzing social issues using structured tools like the Problem Tree method.",
            "With the support of AI, we aim to simplify the process of writing and problem analysis, allowing you to focus on driving meaningful change in your community.",
            "\n<b>Available Commands:</b>",
            "\n/start - Begin a conversation with Raed or restart it.",
            "\n/cancel - End the conversation at any time.",
            "\n/info - Get information about Raed and its features.",
            "\n\n<b>Please confirm your preferred language:</b>",
            "\nType 'English' to continue in English or 'Arabic' to continue in Arabic."
        )),

        'ar': ''.join((
            "<b>مرحبًا بك في رائد، بوت دعم النشطاء!</b>\n",
            "رائد مصمم لمساعدة منظمات المجتمع المدني، النشطاء، وصناع التغيير في إعداد مذكرات مفاهيمية مؤثرة، مقترحات كاملة، وتحليل القضايا الاجتماعية باستخدام أدوات منظمة مثل طريقة شجرة المشكلة.",
            "بدعم من الذكاء الاصطناعي، نسعى لتبسيط عملية الكتابة والتحليل، مما يتيح لك التركيز على تحقيق تغيير حقيقي في مجتمعك.",
            "\n<b>الأوامر المتاحة:</b>",
            "\n/start - بدء محادثة مع رائد أو إعادة تشغيلها.",
            "\n/cancel - إنهاء المحادثة في أي وقت.",
            "\n/info - الحصول على معلومات حول رائد وميزاته.",
            "\n\n<b>يرجى تأكيد لغتك المفضلة:</b>",
            "\nاكتب 'English' للمتابعة باللغة الإنجليزية أو 'Arabic' للمتابعة باللغة العربية."
        ))
    }

    user: User = update.effective_user

    context.user_data['id'] = user.id
    context.user_data['full_name'] = user.full_name
    context.user_data['username'] = user.username

    text: str = define_lang(conversation, user.language_code)

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=ReplyKeyboardMarkup(

            [[
                'English',
                'Arabic'
            ]],
            one_time_keyboard=True,
            resize_keyboard=True
        )
    )

    logger.info(f"User {user.id} ({user.full_name}) started the conversation.")
    return USER_CHOICE_HANDLER
