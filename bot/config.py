#!/usr/bin/env python3
""" """
from dotenv import load_dotenv
import os


# load environment variables from .env file
load_dotenv()
BOT_KEY = os.getenv('API')
GEMINI_KEY = os.getenv("GEMINI_KEY")

# config gemini model
instruction = (
    "you're are a civil society activist in Sudan specialize in writing concept note and proposals for fund rising",
    'your responses should be in arabic'
)


conversation_states = {
    'start': {
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

    },
    'user_type': {
        'en': ''.join((
            "<b>Thank you for choosing your preferred language!</b>\n",
            "Now, please let us know who you are. Are you an activist or representing an organization?",
            "\n\n<b>Options:</b>",
            "\n- Type 'Activist' if you are an individual activist.",
            "\n- Type 'Organization' if you are representing an organization.",
            "\n\nChoose an option to proceed."
        )),

        'ar': ''.join((
            "<b>شكرًا لاختيارك اللغة المفضلة!</b>\n",
            "الآن، يرجى إخبارنا عن هويتك. هل أنت ناشط أم تمثل منظمة؟",
            "\n\n<b>الخيارات:</b>",
            "\n- اكتب 'Activist' إذا كنت ناشطًا.",
            "\n- اكتب 'Organization' إذا كنت تمثل منظمة.",
            "\n\nاختر خيارًا للمتابعة."
        ))

    },
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
        'en': 'Please upload your file in PDF format.',
        'ar': 'يرجى تحميل ملفك بصيغة PDF.'
    },

    'upload_success': {
        'en': "Profile uploaded successfully! Now, choose what you'd like to do:",

        'ar': "تم تحميل الملف الشخصي بنجاح! الآن، اختر ما تريد القيام به:"

    },
    'error_user_type': {
        'en': 'Please select a valid option: Activist or Organization.',
        'ar': 'يرجى اختيار خيار صالح: ناشط أو منظمة.'

    },

    'error_valid_document': {
        'en': "Please upload a valid profile document. Accepted file types are PDF or plain text.",

        'ar': "يرجى تحميل ملف تعريف صالح. أنواع الملفات المقبولة هي PDF أو نص عادي."

    },

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

    'end': {
        'en': "Task completed successfully! If you'd like to restart the bot, type /start. For any suggestions or inquiries, feel free to reach out at hi@mynameisali.tech.",
        'ar': "تم إكمال المهمة بنجاح! إذا كنت ترغب في إعادة تشغيل البوت، اكتب /start. لأي اقتراحات أو استفسارات، لا تتردد في التواصل عبر hi@mynameisali.tech."
    }


}
