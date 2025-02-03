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
from telegram import Update, CallbackQuery
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from logging import getLogger
from ..utils.utilties import define_lang
from .. import PROBLEM_TREE_ANALYSIS, SWOT_ANALYSIS, PESTEL_ANALYSIS

logger = getLogger(__name__)


async def set_analysis_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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
        'PROBLEM_TREE_ANALYSIS': {
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
        'SWOT_ANALYSIS': {
            'en': ''.join([
                '<b>SWOT Analysis 📊</b>\n\n',
                'This tool evaluates:\n',
                '- <u>Strengths</u> (internal advantages) 📈\n',
                '- <u>Weaknesses</u> (internal limitations) 📉\n',
                '- <u>Opportunities</u> (external positive factors) 🌟\n',
                '- <u>Threats</u> (external challenges) 🌪️\n\n',
                '<i>Describe your project/organization/initiative for analysis. ',
                'Example: "A local NGO promoting digital literacy in rural communities."</i>'
            ]),
            'ar': ''.join([
                '<b>تحليل سوات (SWOT) 📊</b>\n\n',
                'تقيم هذه الأداة:\n',
                '- <u>النقاط القوة</u> (مزايا داخلية) 📈\n',
                '- <u>النقاط الضعف</u> (قيود داخلية) 📉\n',
                '- <u>الفرص</u> (عوامل خارجية إيجابية) 🌟\n',
                '- <u>التهديدات</u> (تحديات خارجية) 🌪️\n\n',
                '<i>صف مشروعك/منظمتك/مبادرتك للتحليل. ',
                'مثال: "منظمة محلية تعمل على تعزيز محو الأمية الرقمية في المجتمعات الريفية."</i>'
            ]),
        },
        'PESTEL_ANALYSIS': {
            'en': ''.join([
                '<b>PESTEL Analysis 🌐</b>\n\n',
                'This tool examines external factors affecting your project/organization:\n',
                '- <u>Political</u> (government policies, regulations) 🏛️\n',
                '- <u>Economic</u> (economic trends, market conditions) 💹\n',
                '- <u>Social</u> (cultural trends, demographics) 👥\n',
                '- <u>Technological</u> (innovations, tech advancements) 🚀\n',
                '- <u>Environmental</u> (ecological issues, sustainability) 🌍\n',
                '- <u>Legal</u> (laws, compliance requirements) ⚖️\n\n',
                '<i>Describe your project/organization/initiative for analysis. ',
                'Example: "A startup developing renewable energy solutions."</i>'
            ]),
            'ar': ''.join([
                '<b>تحليل بيستل (PESTEL) 🌐</b>\n\n',
                'تدرس هذه الأداة العوامل الخارجية التي تؤثر على مشروعك/منظمتك:\n',
                '- <u>السياسية</u> (السياسات الحكومية، اللوائح) 🏛️\n',
                '- <u>الاقتصادية</u> (الاتجاهات الاقتصادية، ظروف السوق) 💹\n',
                '- <u>الاجتماعية</u> (الاتجاهات الثقافية، التركيبة السكانية) 👥\n',
                '- <u>التكنولوجية</u> (الابتكارات، التطورات التكنولوجية) 🚀\n',
                '- <u>البيئية</u> (القضايا البيئية، الاستدامة) 🌍\n',
                '- <u>القانونية</u> (القوانين، متطلبات الامتثال) ⚖️\n\n',
                '<i>صف مشروعك/منظمتك/مبادرتك للتحليل. ',
                'مثال: "شركة ناشئة تعمل على تطوير حلول الطاقة المتجددة."</i>'
            ]),
        }
    }

    query: CallbackQuery = update.callback_query
    await query.answer()

    method: str = query.data

    if method == 'PROBLEM_TREE_ANALYSIS':
        await context.bot.send_message(
            text=define_lang(conversation[method],
                             context.user_data['language_code']),
            chat_id=context._chat_id,
            parse_mode=ParseMode.HTML
        )

        logger.info(f"User selected analysis method: {method}")
        return PROBLEM_TREE_ANALYSIS
    elif method == 'SWOT_ANALYSIS':
        await context.bot.send_message(
            text=define_lang(conversation[method],
                             context.user_data['language_code']),
            chat_id=context._chat_id,
            parse_mode=ParseMode.HTML
        )
        logger.info(f"User selected analysis method: {method}")
        return SWOT_ANALYSIS
    elif method == 'PESTEL_ANALYSIS':
        await context.bot.send_message(
            text=define_lang(conversation[method],
                             context.user_data['language_code']),
            chat_id=context._chat_id,
            parse_mode=ParseMode.HTML
        )
        logger.info(f"User selected analysis method: {method}")
        return PESTEL_ANALYSIS
