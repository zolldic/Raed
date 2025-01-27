#!/usr/bin/env python3

"""This module defines the user type selection state for a Telegram bot.

Functions:
    user_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Handles the user's choice of type (activist or organization) and responds accordingly.
"""

from logging import getLogger
from telegram import (
    Update,
    ReplyKeyboardMarkup
)
from telegram.ext import ContextTypes
from ..utils.utilties import define_lang
from .. import CHOICE, CHOOSE_TASK, UPLOAD_PROFILE

logger = getLogger(__name__)


async def user_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the user's choice of either 'Activist' or 'Organization' and responds accordingly.
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.
    Returns:
        int: This function returns different states based on the user's choice:
            - CHOOSE_TASK: If the user selects 'Activist'.
            - UPLOAD_PROFILE: If the user selects 'Organization'.
            - CHOICE: If the user enters an invalid choice.
    """

    user_type: str = update.message.text
    context.user_data['type'] = user_type

    conversation: dict[dict[str]] = {
        'activist': {
            'en': ''.join((
                "<b>Thank you for confirming that you are an activist!</b>\n",
                "As an activist, I can assist you with the following tasks. Please choose one to proceed:",
                "\n\n<b>Options:</b>",
                "\n- Analyze a social problem using the Problem Tree method.",
                "\n- Create a concept note for your project idea.",
                "\n- Write a full proposal for your initiative.",
                "\n\n<b>How to proceed:</b>",
                " Simply reply with one of the following options: 'Analyze Problem', 'Create Concept Note', or 'Write Full Proposal'."
            )),

            'ar': ''.join((
                "<b>شكرًا لتأكيد أنك ناشط!</b>\n",
                "بصفتك ناشطًا، يمكنني مساعدتك في المهام التالية. يرجى اختيار أحد الخيارات للمتابعة:",
                "\n\n<b>الخيارات:</b>",
                "\n- تحليل مشكلة اجتماعية باستخدام طريقة شجرة المشكلة.",
                "\n- إنشاء مذكرة مفهوم لفكرة مشروعك.",
                "\n- كتابة مقترح كامل لمبادرتك.",
                "\n\n<b>كيفية المتابعة:</b>",
                " ببساطة، قم بالرد بأحد الخيارات التالية: 'Analyze Problem' أو 'Create Concept Note' أو 'Write Full Proposal'."
            )),
        },
        'organization': {
            'en': ''.join((
                "<b>Thank you for confirming that you represent an organization!</b>\n",
                "To get started, please upload your organization's profile as a PDF, DOCX, or DOC file. ",
            )),
            'ar': ''.join((
                "<b>شكرًا لتأكيد أنك تمثل منظمة!</b>\n",
                "للبدء، يرجى تحميل ملف تعريف المنظمة كملف PDF أو DOCX أو DOC. ",
            )),
        },
        'error': {
            'en': "Sorry, I didn't understand that. Please choose either 'Activist' or 'Organization'.",
            'ar': "عذرًا، لم أفهم ذلك. يرجى اختيار 'ناشط' أو 'منظمة'."
        }
    }

    text: str = ''

    if user_type == "Activist":
        text = define_lang(
            conversation['activist'], context.user_data['language_code']
        )

        await update.message.reply_text(
            text,
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(
                [[
                    'Analyze a problem',
                    'Create a concept note',
                    'Write a full proposal'
                ]],
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )

        logger.info(f"User selected {user_type}. Proceeding to CHOOSE_TASK.")

        return CHOOSE_TASK
    elif user_type == "Organization":
        text = define_lang(
            conversation['organization'], context.user_data['language_code']
        )
        await update.message.reply_text(
            text,
            parse_mode='HTML'
        )

        logger.info(
            f"User selected {user_type}. Proceeding to UPLOAD_PROFILE.")

        return UPLOAD_PROFILE
    else:
        text = define_lang(
            conversation['error'], context.user_data['language_code'])

        await update.message.reply_text(
            text,
            parse_mode='HTML')

        logger.info(f"Invalid choice entered by user: '{user_type}'")

        return CHOICE
