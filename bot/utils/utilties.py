#!/usr/bin/env python3
"""This module provides utility functions for language definition and text extraction from PDF files.

Functions:
    define_lang(texts, user_language) -> str:
        Defines the language based on the user's language preference.

    extract_text_from_file(buf, file_name) -> str:
        Extracts and returns text content from a PDF, DOCX and DOC file.
    
    verify_file_format(file_name) -> bool:
        Verifies the format of the uploaded file.
"""

from pypdf import PdfReader
from docx import Document
import textract


def define_lang(texts: dict, lang: str) -> str:
    """Defines the language based on the user's language preference
    Returns:
        str: the text in the user's lanaguage preference
    """
    try:
        return texts[lang]
    except KeyError:
        return None


def extract_text_from_file(buf: bytearray, file_name: str) -> str:
    """Extracts and returns text content from a PDF, DOCX and DOC file.

    Args:
        buf (bytearray): buffer represent the file content as bytes
        file_name (str): the name of the file

    Returns:
        str: the content of the file
    """

    ext = file_name.split('.')[1]
    match ext.lower():
        case 'pdf':
            reader = PdfReader(buf)
            return ''.join(
                [page.extract_text() or "" for page in reader.pages]
            )
        case 'docx':
            document = Document(buf)
            return ''.join(
                [paragraph.text for paragraph in document.paragraphs]
            )
        case 'doc':
            return textract.process(buf, extension='doc').decode('utf-8')


def verify_file_format(file_name: str) -> bool:
    """Verifies the format of the uploaded file.

        Args:
            file_name (str): The name of the uploaded file.

        Returns:
            bool: True if the file format is valid, False otherwise.
    """
    allowed_ext: set[str] = {'pdf', 'docx', 'doc'}
    return any(file_name.endswith(ext) for ext in allowed_ext)
