import contextlib
import importlib
import io
import unittest
from unittest.mock import patch
from email_regex import validate_email, validate_phone
from final_project import Final, main


class Tests(unittest.TestCase):
    def exercise(self,method,answers):
        output=io.StringIO()
        with patch('builtins.input',side_effect=answers),contextlib.redirect_stdout(output):
            getattr(Final(),method)()
        return output.getvalue()
    def test_emails(self):
        for value in ('name+tag@example.com','a.b@sub.example.co','a@domain0.com'):
            self.assertIs(validate_email(value),True)
        for value in ('a..b@example.com','.a@example.com','a@-bad.com','a@example.com\n','a@b.c','a'*65+'@example.com',None):
            self.assertIs(validate_email(value),False)
    def test_phones(self):
        for value in ('09123456789','+989123456789','00989123456789'):
            self.assertIs(validate_phone(value),True)
        for value in ('123','09123456789\n','۰۹۱۲۳۴۵۶۷۸۹','0912345678',None):
            self.assertIs(validate_phone(value),False)
    def test_factorial_and_fibonacci(self):
        self.assertEqual(self.exercise('p3',['0']).strip(),'1')
        self.assertEqual(self.exercise('p3',['6']).strip(),'720')
        self.assertEqual(self.exercise('p4',['6']).strip(),'1;1;2;3;5;8;')
        with self.assertRaises(ValueError):self.exercise('p3',['-1'])
    def test_codepoints_case_and_decode(self):
        self.assertEqual(self.exercise('p8',['Ab','encode']).strip(),'65, 98')
        self.assertEqual(self.exercise('p8',['65,98','decode']).strip(),'Ab')
    def test_sms_keymap(self):
        output=self.exercise('p10',['defwxyz'])
        self.assertIn('3: 6',output);self.assertIn('9: 10',output)
        with self.assertRaises(ValueError):self.exercise('p10',['!'])
    def test_geometry(self):
        self.assertEqual(self.exercise('p5',['rectangle','area','3','4']).strip(),'12')
        with self.assertRaises(ValueError):self.exercise('p5',['circle','area','-2'])
    def test_coursework_exceptions_retained(self):
        with self.assertRaises(ValueError):self.exercise('p3',['5'])
        with self.assertRaises(TypeError):self.exercise('p1',['1','15'])
        with self.assertRaises(Exception):self.exercise('p4',['8'])
    def test_no_import_side_effect_and_clean_eof(self):
        with patch('builtins.input',side_effect=AssertionError('input on import')):
            import final_project
            importlib.reload(final_project)
        with patch('builtins.input',side_effect=EOFError),contextlib.redirect_stdout(io.StringIO()):main()


if __name__=='__main__':unittest.main()
