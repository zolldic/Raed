#!/usr/bin/env python3
"""Handles user task selection and transitions to the appropriate state based on the selected task.
"""

import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from ..utils.utilties import define_lang
from .. import (USER_CHOICE_HANDLER, CONVERSATION_HANDLER,
                ANALYSIS_TOOLS, USER_ROLE)

logger = logging.getLogger(__name__)


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """This function processes the user's message to determine the selected task. It validates the task choice
    and transitions to the corresponding state. If the task choice is invalid, it sends an error message and
    returns to the user choice handler state.

    Args:
        update (telegram.Update): The update object that contains the user's message.
        context (telegram.ext.ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.

    Returns:
        int: The next state to transition to based on the user's task selection.
    """
    conversaion: dict[str] = {
        'analysis_tools': {
            'en': ''.join([
                '<b>Analysis Tools Overview 🔍</b>\n\n',
                'Please choose an analysis method:\n\n',
                '1. <u>Problem Tree Method</u> 🌳\n',
                '   - Identifies root causes, effects, and core issues\n\n',
                '2. <u>SWOT Analysis</u> 📊\n',
                '   - Evaluates Strengths, Weaknesses, Opportunities, Threats\n\n',
                '3. <u>PESTEL Analysis</u> 🌐\n',
                '   - Examines Political, Economic, Social, Technological, Environmental, Legal factors\n\n',
                '<i>Type the number of your preferred method.</i>'
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
                '<i>اكتب رقم الأداة التي تفضلها.</i>'
            ])
        },
        'concept_note': {
            'en': ''.join([
                '<b>Concept Note 📄</b>\n\n'
                'A concise document summarizing a project\'s purpose, objectives, and expected impact. '
                'Used to pitch ideas to stakeholders or funders.\n\n'
                '<b>Are you an individual activist or representing an organization?</b>\n\n'
                '1. Individual Activist 👤\n'
                '2. Organization 🏢\n\n'
                '<i>Type the number of your role.</i>'
            ]),
            'ar': ''.join([
                '<b>مذكرة مفاهيمية 📄</b>\n\n'
                'مذكرة موجزة تُلخص الغرض، الأهداف، والأثر المتوقع للمشروع. تُستخدم لعرض الأفكار على أصحاب المصلحة أو الممولين.\n\n'
                '<b>هل أنت ناشط فردي أم تمثل منظمة؟</b>\n\n'
                '1. ناشط فردي 👤\n'
                '2. منظمة 🏢\n\n'
                '<i>اكتب رقم الدور الخاص بك.</i>'])
        },
        'full_proposal': {
            'en': ''.join(['<b>Full Proposal 📑</b>\n\n'
                           'A comprehensive document detailing project methodology, budget, timeline, and implementation plan. '
                           'Required for formal funding applications.\n\n'
                           '<b>Are you an individual activist or representing an organization?</b>\n\n'
                           '1. Individual Activist 👤\n'
                           '2. Organization 🏢\n\n'
                           '<i>Type the number of your role.</i>'
                           ]),

            'ar': ''.join([
                '<b>مقترح كامل 📑</b>\n\n'
                'وثيقة تفصيلية تشمل منهجية المشروع، الميزانية، الجدول الزمني، وخطة التنفيذ. مطلوبة لطلبات التمويل الرسمية.\n\n'
                '<b>هل أنت ناشط فردي أم تمثل منظمة؟</b>\n\n'
                '1. ناشط فردي 👤\n'
                '2. منظمة 🏢\n\n'
                '<i>اكتب رقم الدور الخاص بك.</i>'
            ])
        },
        'error': {
            'en': '<b>Invalid task choice. Please select a valid task.</b>',
            'ar': '< b > اختيار مهمة غير صالح. الرجاء اختيار مهمة صالحة. < /b'
        }
    }

    tasks: set = {
        'Analysis Tools',
        'Generate Concept Note',
        'Generate Full Proposal'
    }

    if update.message.text not in tasks:
        await update.message.reply_text(
            define_lang(
                conversaion['error'],
                context.user_data['language_code']),
            parse_mode='HTML',
            reply_markup=ReplyKeyboardMarkup(
                [[
                    'Analysis Tools',
                    'Generate Concept Note',
                    'Generate Full Proposal'
                ]],
                one_time_keyboard=True,
                resize_keyboard=True)
        )
        logger.warning(
            f"Invalid task choice: {update.message.text}. Returning to USER_CHOICE_HANDLER state.")
        return CONVERSATION_HANDLER

    context.user_data['task'] = update.message.text

    match context.user_data['task']:
        case 'Analysis Tools':
            await update.message.reply_text(
                define_lang(
                    conversaion['analysis_tools'],
                    context.user_data['language_code']),
                parse_mode='HTML',
                reply_markup=ReplyKeyboardMarkup(
                    [
                        ['1', '2', '3']
                    ],
                    one_time_keyboard=True,
                    resize_keyboard=True)
            )
            logger.info(
                "User selected 'Analysis Tools'. Transitioning to ANALYSIS_TOOLS state.")
            return ANALYSIS_TOOLS
        case 'Generate Concept Note':
            await update.message.reply_text(
                define_lang(conversaion['concept_note'],
                            context.user_data['language_code']),
                parse_mode='HTML',
                reply_markup=ReplyKeyboardMarkup(
                    [
                        ['1', '2']
                    ],
                    one_time_keyboard=True,
                    resize_keyboard=True)

            )
            logger.info(
                "User selected 'Generate Concept Note'. Transitioning to CONCEPT_NOTE state")
            return USER_ROLE
        case 'Generate Full Proposal':
            await update.message.reply_text(
                define_lang(
                    conversaion['full_proposal'],
                    context.user_data['language_code']),
                parse_mode='HTML',
                reply_markup=ReplyKeyboardMarkup(
                    [
                        ['1', '2']
                    ],
                    one_time_keyboard=True,
                    resize_keyboard=True)
            )
            logger.info(
                "User selected 'Generate Full Proposal'. Transitioning to FULL_PROPOSAL state.")
            return USER_ROLE
        case _:  # This should never be reached
            logger.error(
                "Invalid task choice. Returning to USER_CHOICE_HANDLER state.")
            return USER_CHOICE_HANDLER
