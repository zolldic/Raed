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
                '<b>SWOT Analysis for Civil Society Organizations & Activists ✊🔍</b>\n\n',
                'This tool helps assess the <u>Strengths</u>, <u>Weaknesses</u>, <u>Opportunities</u>, ',
                'and <u>Threats</u> affecting your organization, campaign, or initiative. It is essential ',
                'for strategic planning, advocacy efforts, and sustainability.\n\n',
                '<i>Please describe the focus of your SWOT analysis. For example: "A grassroots campaign for climate justice" or "A human rights NGO working in conflict zones."</i>'
            ]),
            'ar': ''.join([
                '<b>تحليل سوات (SWOT) لمنظمات المجتمع المدني والنشطاء ✊🔍</b>\n\n',
                'تساعد هذه الأداة في تقييم <u>نقاط القوة</u> و<u>نقاط الضعف</u> و<u>الفرص</u> ',
                'و<u>التهديدات</u> التي تؤثر على منظمتك أو حملتك أو مبادرتك. أداة أساسية ',
                'للتخطيط الاستراتيجي، وجهود المناصرة، وضمان الاستدامة.\n\n',
                '<i>يرجى تحديد مجال تحليل سوات الخاص بك. على سبيل المثال: "حملة شعبية للعدالة المناخية" أو "منظمة حقوقية تعمل في مناطق النزاع".</i>'
            ])
        },
        'pestel_analysis': {
            'en': ''.join([
                '<b>PESTEL Analysis for Civil Society Organizations & Activists 🌍⚖️</b>\n\n',
                'This framework evaluates external factors influencing your work, including:\n',
                '- <u>Political</u>: Government policies, freedom of expression, civic space.\n',
                '- <u>Economic</u>: Funding availability, donor priorities, financial sustainability.\n',
                '- <u>Social</u>: Public awareness, community support, social movements.\n',
                '- <u>Technological</u>: Digital security, online activism, access to tools.\n',
                '- <u>Environmental</u>: Climate challenges, sustainability concerns, green initiatives.\n',
                '- <u>Legal</u>: Laws on NGOs, human rights frameworks, regulatory barriers.\n\n',
                '<i>Please specify the issue or context for your PESTEL analysis. For example: "The impact of restrictive NGO laws" or "The role of technology in human rights advocacy."</i>'
            ]),
            'ar': ''.join([
                '<b>تحليل بيستل (PESTEL) لمنظمات المجتمع المدني والنشطاء 🌍⚖️</b>\n\n',
                'يقوم هذا الإطار بتقييم العوامل الخارجية التي تؤثر على عملك، بما في ذلك:\n',
                '- <u>السياسية</u>: السياسات الحكومية، حرية التعبير، الفضاء المدني.\n',
                '- <u>الاقتصادية</u>: توفر التمويل، أولويات المانحين، الاستدامة المالية.\n',
                '- <u>الاجتماعية</u>: وعي المجتمع، دعم الجمهور، الحركات الاجتماعية.\n',
                '- <u>التكنولوجية</u>: الأمن الرقمي، النشاط الإلكتروني، الوصول إلى الأدوات.\n',
                '- <u>البيئية</u>: تحديات المناخ، قضايا الاستدامة، المبادرات الخضراء.\n',
                '- <u>القانونية</u>: قوانين المنظمات غير الحكومية، أطر حقوق الإنسان، العوائق التنظيمية.\n\n',
                '<i>يرجى تحديد القضية أو السياق الخاص بتحليلك البيستل. على سبيل المثال: "تأثير القوانين المقيدة للمنظمات غير الحكومية" أو "دور التكنولوجيا في الدفاع عن حقوق الإنسان".</i>'
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
        logger.warning("Invalid analysis method selected.")
        return ANALYSIS_TOOLS
