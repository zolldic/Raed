#!/usr/bin/env python3

import unittest
from bot.utils.utilties import define_lang, verify_file_format, check_size


class TestUtilties(unittest.TestCase):
    """ """

    def test_define_lang(self):
        """ """
        texts = {'en': 'Hello', 'ar': 'مرحبا'}
        self.assertEqual(define_lang(texts, 'en'), 'Hello')
        self.assertEqual(define_lang(texts, 'ar'), 'مرحبا')
        self.assertEqual(define_lang(texts, 'fr'), None)

    def test_check_file_size(self):

        self.assertFalse(check_size(1000000))

    def test_verify_file_format(self):
        """
        """
        self.assertTrue(verify_file_format('hello.pdf'))
        self.assertTrue(verify_file_format('hello.docx'))
        self.assertTrue(verify_file_format('hello.doc'))

        self.assertFalse(verify_file_format('hello.txt'), False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
