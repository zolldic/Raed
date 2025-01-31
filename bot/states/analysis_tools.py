#!/usr/bin/env python3
"""This module provides functionality for choosing different analysis methods
via a Telegram bot. The available methods include Problem Tree Analysis,
SWOT Analysis, and PESTEL Analysis. The module defines a function to handle
user input and respond with the appropriate analysis method description
based on the user's selection and language preference.

Functions:
    choose_analysis_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        Handles user input to choose an analysis method and responds with
        the corresponding description in the user's preferred language.
"""
from telegram import Update
from telegram.ext import ContextTypes
from logging import getLogger
from ..utils.utilties import define_lang
from .. import (
    ANALYSIS_TOOLS, PROBLEM_TREE_ANALYSIS,
    SWOT_ANALYSIS, PESTEL_ANALYSIS,
)

logger = getLogger(__name__)


async def choose_analysis_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the selection of an analysis method and sends the corresponding information to the user.
    This function processes the user's input to determine which analysis method they have chosen.
    It then sends a detailed description of the selected method in the user's preferred language.
    The available analysis methods are:
        1. Problem Tree Method
        2. SWOT Analysis
        3. PESTEL Analysis
    Args:
        update (Update): The update object that contains the user's message.
        context (ContextTypes.DEFAULT_TYPE): The context object that contains user data and other information.
    Returns:
        int: The next state in the conversation, which corresponds to the chosen analysis method.
    """

    conversation: dict[str, str] = {
        'problem_tree_method': {
            'en': ''.join([
                '<b>Problem Tree Method 🌳</b>\n\n',
                'This tool helps visualize the <u>root causes</u> (roots), <u>core problem</u> (trunk), ',
                'and <u>effects</u> (branches) of an issue. Ideal for identifying systemic drivers and planning interventions.\n\n',
                '<i>Please describe the problem you want to analyze. For example: "Lack of clean water in rural areas."</i>'
            ]),
            'ar': ''.join([
                '<b>طريقة شجرة المشكلة 🌳</b>\n\n',
                'تساعد هذه الأداة في تحديد <u>الأسباب الجذرية</u> (الجذور)، <u>المشكلة الأساسية</u> (الجذع)، ',
                'و<u>الآثار</u> (الفروع) لقضية ما. مثالية لفهم العوامل النظامية والتخطيط للحلول.\n\n',
                '<i>الرجاء وصف المشكلة التي تريد تحليلها. مثال: "نقص المياه النظيفة في المناطق الريفية."</i>'
            ]),
        },
        'swot_analysis': {
            'en': ''.join([
                '<b>SWOT Analysis 🔍</b>\n\n',
                'This tool helps assess the <u>Strengths</u>, <u>Weaknesses</u>, <u>Opportunities</u>, ',
                'and <u>Threats</u> related to a project, organization, or situation. Ideal for strategic planning and decision-making.\n\n',
                '<i>Please specify the subject of your SWOT analysis. For example: "A new product launch in the tech industry."</i>'
            ]),
            'ar': ''.join([
                '<b>تحليل سوات (SWOT) 🔍</b>\n\n',
                'يساعد هذا الأداة في تقييم <u>نقاط القوة</u> و<u>نقاط الضعف</u> و<u>الفرص</u> ',
                'و<u>التهديدات</u> المتعلقة بمشروع أو منظمة أو موقف معين. مثالي للتخطيط الاستراتيجي واتخاذ القرارات.\n\n',
                '<i>يرجى تحديد موضوع تحليل سوات الخاص بك. على سبيل المثال: "إطلاق منتج جديد في صناعة التكنولوجيا".</i>'
            ])
        },
        'pestel_analysis': {
            'en': ''.join([
                '<b>PESTEL Analysis 🌍</b>\n\n',
                'This framework evaluates the external <u>Political</u>, <u>Economic</u>, <u>Social</u>, <u>Technological</u>, ',
                '<u>Environmental</u>, and <u>Legal</u> factors affecting a business or initiative. Essential for understanding macro-level influences.\n\n',
                '<i>Please specify the industry or business environment you want to analyze. For example: "The renewable energy sector."</i>'
            ]),
            'ar': ''.join([
                '<b>تحليل بيستل (PESTEL) 🌍</b>\n\n',
                'يقوم هذا الإطار بتقييم العوامل الخارجية <u>السياسية</u> و<u>الاقتصادية</u> و<u>الاجتماعية</u> و<u>التكنولوجية</u> ',
                'و<u>البيئية</u> و<u>القانونية</u> التي تؤثر على الأعمال أو المبادرات. أداة أساسية لفهم التأثيرات على المستوى الكلي.\n\n',
                '<i>يرجى تحديد الصناعة أو بيئة العمل التي تريد تحليلها. على سبيل المثال: "قطاع الطاقة المتجددة".</i>'
            ])
        }
    }

    method: str = update.message.text
    if method == '1':
        await update.message.reply_text(
            define_lang(conversation['problem_tree_method'],
                        context.user_data['language_code']
                        ),
            parse_mode='HTML'
        )

        logger.info("User selected Problem Tree Method")
        return PROBLEM_TREE_ANALYSIS
    elif method == '2':
        await update.message.reply_text(
            define_lang(conversation['swot_analysis'],
                        context.user_data['language_code']
                        ),
            parse_mode='HTML'
        )

        logger.info("User selected SWOT Analysis")
        return SWOT_ANALYSIS
    elif method == '3':
        await update.message.reply_text(
            define_lang(conversation['pestel_analysis'],
                        context.user_data['language_code']
                        ),
            parse_mode='HTML'
        )

        logger.info("User selected PESTEL Analysis")
        return PESTEL_ANALYSIS
    else:
        logger.warning("Invalid analysis method selected."))
        return ANALYSIS_TOOLS
