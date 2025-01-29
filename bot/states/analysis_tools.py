#!/usr/bin/env python3

from telegram import (
    Update, ReplyKeyboardMarkup
)
from telegram.ext import (
    ContextTypes,
)
from logging import getLogger
from ..utils.utilties import define_lang
from .. import (
    ANALYSIS_TOOLS, PROBLEM_TREE_ANALYSIS,
    SWOT_ANALYSIS, PESTEL_ANALYSIS,
    FLOW_HANDLER
)
from ..gemini.analysis import analysis_model

logger = getLogger(__name__)


async def choose_analysis_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
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

        },
        'pestel_analysis': {}
    }
    method: str = update.message.text

    if method == '1':
        await update.message.reply_text(
            define_lang(conversation['problem_tree_method'],
                        context.user_data['language_code']
                        ),
            parse_mode='HTML'
        )
        return PROBLEM_TREE_ANALYSIS
    elif method == '2':
        return SWOT_ANALYSIS
    elif method == '3':
        return PESTEL_ANALYSIS
    else:
        return ANALYSIS_TOOLS
