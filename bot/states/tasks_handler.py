#!/usr/bin/env python3
"""Handles user task selection and transitions to the appropriate state based on the selected task.
"""

import logging
from telegram import (
    Update, CallbackQuery,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from ..utils.utilties import define_lang
from .. import ANALYSIS_TOOLS, SET_PAPER

logger = logging.getLogger(__name__)


async def set_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This function processes the user's message to determine the selected task. It validates the task choice
    and transitions to the corresponding state.

    Args:
        update (telegram.Update): The update object that contains the user's message.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.

    Returns:
        int: The next state to transition to based on the user's task selection.
    """

    query: CallbackQuery = update.callback_query
    await query.answer()
    task: str = query.data

    conversaion: dict[str, str] = {
        'query': {
            'en': f'Your task has been set to: {task.replace("_", " ").lower()}. ✅',
            'ar': f'تم تعيين المهمة إلى: {task.replace("_", " ").lower()}. ✅'
        },
        'ANALYSIS_TOOLS': {
            'en': ''.join([
                '<b>Analysis Tools Overview 🔍</b>\n\n',
                'Please choose an analysis method:\n\n',
                '1. <u>Problem Tree Method</u> 🌳\n',
                '   - Identifies root causes, effects, and core issues\n\n',
                '2. <u>SWOT Analysis</u> 📊\n',
                '   - Evaluates Strengths, Weaknesses, Opportunities, Threats\n\n',
                '3. <u>PESTEL Analysis</u> 🌐\n',
                '   - Examines Political, Economic, Social, Technological, Environmental, Legal factors\n\n',
            ]),
            'ar': ''.join([
                '<b>نظرة عامة على أدوات التحليل 🔍</b>\n\n',
                'الرجاء اختيار أداة التحليل:\n\n',
                '1. <u>طريقة شجرة المشكلة</u> 🌳\n',
                '   - تحدد الأسباب الجذرية، الآثار، والقضايا الأساسية\n\n',
                '2. <u>تحليل سوات (SWOT)</u> 📊\n',
                '   - يقيم النقاط القوة، الضعف، الفرص، التهديدات\n\n',
                '3. <u>تحليل بيستل (PESTEL)</u> 🌐\n',
                '   - يدرس العوامل السياسية، الاقتصادية، الاجتماعية، التكنولوجية، البيئية، القانونية\n\n',
            ])
        },

        'CONCEPT_NOTE': {
            'en': ''.join([
                '<b>Would you like to upload a document (e.g., organization profile) to adjust the response?</b>\n',

            ]),
            'ar': ''.join([
                '<b>هل ترغب في تحميل مستند (مثل ملف تعريف المنظمة) لتعديل الرد بناءً عليه؟</b>\n',
            ])
        },
        'END': {
            'en': 'Thank you for using Raed. Have a great day! 👋',
            'ar': 'شكرًا لاستخدام رائد. أتمنى لك يومًا سعيدًا! 👋'

        }
    }

    await query.edit_message_text(
        define_lang(conversaion['query'], context.user_data['language_code'])
    )
    if task == 'ANALYSIS_TOOLS':
        await context.bot.send_message(
            text=define_lang(
                conversaion[task], context.user_data['language_code']
            ),
            chat_id=context._chat_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            'Problem Tree Method', callback_data='PROBLEM_TREE_ANALYSIS')
                    ],
                    [
                        InlineKeyboardButton(
                            'SWOT Analysis', callback_data='SWOT_ANALYSIS')
                    ],
                    [
                        InlineKeyboardButton(
                            'PESTEL Analysis', callback_data='PESTEL_ANALYSIS')
                    ]
                ]
            ),
            parse_mode=ParseMode.HTML
        )
        logger.info(
            f"User {update.effective_user.id} selected Analysis Tools task.")
        return ANALYSIS_TOOLS
    elif task == 'CONCEPT_NOTE':
        await context.bot.send_message(
            text=define_lang(
                conversaion[task], context.user_data['language_code']
            ),
            chat_id=context._chat_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            'Yes ✅', callback_data='Yes')
                    ],
                    [
                        InlineKeyboardButton(
                            'No ❌', callback_data='No')
                    ],
                ]
            ),
            parse_mode=ParseMode.HTML
        )

        logger.info(
            f"User {update.effective_user.id} selected Concept Note task.")
        return SET_PAPER
    else:
        message: str = define_lang(
            conversaion['END'], context.user_data['language_code'])
        await context.bot.send_message(
            text=message,
            chat_id=context._chat_id,
        )

        logger.info(f"User {update.effective_user.id} selected task: {task}")
        ConversationHandler.END
