import argparse
import base64
import getpass
import hashlib
import hmac
import math
import pyperclip
import scrypt
import sys
import time


def gen_password(master_pw, user_id, n):
    hmac_key = scrypt.hash(master_pw, 'zerostore-salt'+user_id, N=16384, r=8, p=1, buflen=64)
    digest = hmac.HMAC(hmac_key, user_id, hashlib.sha256).digest()
    return base64.b64encode(digest)[:n]


def main():
    parser = argparse.ArgumentParser(description='Generate secure, unique passwords based on a master password.')

    parser.add_argument('-n', '--len', dest='n', default=24, type=int,
        help='The length of the password to generate. Defaults to 24, maximum 44')

    args = parser.parse_args()

    if args.n > 44:
        print 'Sorry, passwords with a length greater than 32 are not currently supported.'
        sys.exit(1)

    user_id = raw_input('account id: ')
    master_pw = getpass.getpass('password: ')

    pw = gen_password(master_pw, user_id, args.n)

    pyperclip.copy(pw)
    print 'Password copied to clipboard'

    time.sleep(10)

    pyperclip.copy('[cleared]')
    print 'Clipboard cleared'


if __name__ == '__main__':
    main()
