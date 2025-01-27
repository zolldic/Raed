#!/usr/bin/env python3
"""This module defines the `choose_task` function which processes the user's task selection
and transitions to the appropriate state based on their choice.

Functions:
    choose_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        Handles the user's task selection and transitions to the appropriate state.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
from ..utils.utilties import define_lang
from .. import CHOICE, CHOOSE_TASK, ANALYZE_PROBLEM, CREATE_NOTE, WRITE_PROPOSAL

logger = logging.getLogger(__name__)


async def choose_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handles the user's task selection and transitions
        to the appropriate state based on their choice

        Args:
            update (telegram.Update): Incoming update object containing the user's message and metadata.
            context (telegram.ext.ContextTypes.DEFAULT_TYPE): Context object for storing user-specific data.

        Returns:
            int: The next conversation state (
                ANALYZE_PROBLEM,
                CREATE_NOTE,
                WRITE_PROPOSAL or CHOOSE_TASK
                ).
    """

    conversation: dict[dict[str]] = {
        'analyze_problem': {
            'en': ''.join((
                "<b>Analyze a Problem</b>\n",
                "The Problem Tree method is a tool used to analyze social problems by identifying their root causes and effects. ",
                "It helps break down complex issues into smaller components, making them easier to understand and address effectively.\n",
                "To get started, please describe the social problem you want to analyze in as much detail as possible. ",
                "Include key aspects such as who is affected, where the problem occurs, and any underlying causes you are already aware of."
            )),

            'ar': ''.join((
                "<b>تحليل مشكلة</b>\n",
                "طريقة شجرة المشكلة هي أداة تُستخدم لتحليل القضايا الاجتماعية من خلال تحديد أسبابها الجذرية وآثارها. ",
                "تساعد هذه الطريقة على تفكيك المشكلات المعقدة إلى مكونات أصغر، مما يجعلها أسهل في الفهم والمعالجة بشكل فعال.\n",
                "للبدء، يرجى وصف المشكلة الاجتماعية التي تريد تحليلها بأكبر قدر ممكن من التفاصيل. ",
                "قم بتضمين الجوانب الرئيسية مثل من هم المتأثرون، وأين تحدث المشكلة، وأي أسباب كامنة تعرفها بالفعل."
            ))
        },

        'concept_note': {
            'en': ''.join((
                "<b>Create a Concept Note</b>\n",
                "A concept note is a brief document that outlines the key ideas of a proposed project. ",
                "It is typically used to summarize the project’s objectives, target audience, expected outcomes, ",
                "and activities in a concise way. Concept notes are often the first step in seeking support or funding ",
                "from donors or stakeholders.\n",
                "To begin, please share the topic or main idea of your project and any key details you would like to include in the concept note."
            )),

            'ar': ''.join((
                "<b>إنشاء مذكرة مفهوم</b>\n",
                "مذكرة المفهوم هي وثيقة مختصرة تحدد الأفكار الرئيسية لمشروع مقترح. ",
                "تُستخدم عادةً لتلخيص أهداف المشروع، الجمهور المستهدف، النتائج المتوقعة، ",
                "والأنشطة بطريقة موجزة. تُعتبر مذكرات المفهوم غالبًا الخطوة الأولى للحصول على ",
                "الدعم أو التمويل من المانحين أو أصحاب المصلحة.\n",
                "للبدء، يرجى مشاركة موضوع أو الفكرة الرئيسية لمشروعك وأي تفاصيل رئيسية تريد تضمينها في مذكرة المفهوم."
            ))
        },

        'full_proposal': {
            'en': ''.join((
                "<b>Write a Full Proposal</b>\n",
                "A full proposal is a comprehensive document that provides detailed information about a project. ",
                "It typically includes the problem statement, project objectives, methodology, timeline, budget, and expected outcomes. ",
                "Proposals are used to secure funding or approval for a project and must be clear, detailed, and persuasive.\n",
                "To begin, please share an overview of your project idea, including the social issue it addresses and any initial thoughts on how the project will be implemented."
            )),

            'ar': ''.join((
                "<b>كتابة مقترح كامل</b>\n",
                "المقترح الكامل هو وثيقة شاملة تقدم معلومات تفصيلية حول المشروع. ",
                "يتضمن عادةً بيان المشكلة، أهداف المشروع، المنهجية، الجدول الزمني، الميزانية، والنتائج المتوقعة. ",
                "تُستخدم المقترحات للحصول على التمويل أو الموافقة على المشروع ويجب أن تكون واضحة، تفصيلية، ومقنعة.\n",
                "للبدء، يرجى مشاركة نظرة عامة حول فكرة مشروعك، بما في ذلك القضية الاجتماعية التي يعالجها وأي أفكار أولية حول كيفية تنفيذ المشروع."
            ))

        },

        'invalid_choice': {
            'en': 'Invalid choice. Please choose one of the provided options.',
            'ar': 'خيار غير صالح. يرجى اختيار أحد الخيارات المقدمة.'
        },
    }

    tasks: set = {
        'Analyze a problem',
        'Create a concept note',
        'Write a full proposal'
    }

    task: str = update.message.text
    if task not in tasks:
        text: str = define_lang(
            conversation['invalid_choice'], context.user_data['language_code'])
        update.message.reply_text(
            text,
            parse_mode='HTML'
        )
        logger.warning(
            f"Invalid task choice: {task}. Returning to CHOICE state.")
        return CHOICE

    context.user_data['task'] = task

    text: str = ''
    match task:
        case "Analyze a problem":
            text = define_lang(
                conversation['analyze_problem'], context.user_data['language_code'])
            await update.message.reply_text(
                text,
                parse_mode='HTML'
            )

            logger.info(
                "User selected 'Analyze a problem'. Transitioning to ANALYZE_PROBLEM state.")
            return ANALYZE_PROBLEM
        case "Create a concept note":
            text = define_lang(
                conversation['concept_note'], context.user_data['language_code'])
            await update.message.reply_text(
                text,
                parse_mode='HTML'
            )
            logger.info(
                "User selected 'Create a concept note'. Transitioning to CREATE_NOTE state.")
            return CREATE_NOTE
        case "Write a full proposal":
            text = define_lang(
                conversation['full_proposal'], context.user_data['language_code'])
            await update.message.reply_text(
                text,
                parse_mode='HTML'
            )

            logger.info(
                "User selected 'Write a full proposal'. Transitioning to WRITE_PROPOSAL state.")
            return WRITE_PROPOSAL
        case _:
            text = define_lang(
                conversation['invalid_choice'], context.user_data['language_code'])
            await update.message.reply_text(
                text,
                parse_mode='HTML'
            )
            logger.warning(
                f"User provided an invalid choice: {task}. Returning to CHOOSE_TASK state.")
            return CHOOSE_TASK
