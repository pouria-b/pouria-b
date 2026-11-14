"""Practical ASCII email-shape and Iranian mobile-number format checks.

These checks do not verify that an address/number exists or is reachable.
"""
import argparse
import re

_LOCAL = r'[A-Za-z0-9_+%\-]+(?:\.[A-Za-z0-9_+%\-]+)*'
_LABEL = r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?'
_EMAIL = re.compile(_LOCAL + '@' + _LABEL + r'(?:\.' + _LABEL + r')*\.[A-Za-z]{2,63}')
_PHONE = re.compile(r'(?:09[0-9]{9}|\+989[0-9]{9}|00989[0-9]{9})')


def validate_email(email: str) -> bool:
    if not isinstance(email,str) or len(email)>254:
        return False
    return bool(_EMAIL.fullmatch(email)) and len(email.split('@',1)[0])<=64


def validate_phone(number: str) -> bool:
    return isinstance(number,str) and _PHONE.fullmatch(number) is not None


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('kind',choices=['email','phone'])
    parser.add_argument('value')
    args=parser.parse_args()
    print(validate_email(args.value) if args.kind=='email' else validate_phone(args.value))


if __name__=='__main__':
    main()
