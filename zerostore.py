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

from string import printable

parser = argparse.ArgumentParser(description='Generate secure, unique passwords based on a master password.')

parser.add_argument('-n', '--len', dest='n', default=24, type=int,
    help='The length of the password to generate. Defaults to 24, maximum 32')

parser.add_argument('-c', '--charset', dest='charset', default=printable,
    help='The character set to use when generating the password. Defaults to all printable characters.')

args = parser.parse_args()

def gen_password(master_pw, user_id):
    hmac_key = scrypt.hash(master_pw, 'zerostore-salt'+user_id, N=16384, r=8, p=1, buflen=64)
    digest = hmac.HMAC(hmac_key, user_id, hashlib.sha256).digest()
    return ''.join(args.charset[ord(c) % len(args.charset)] for c in digest[:args.n])

if args.n > 32:
    print 'Sorry, passwords with a length greater than 32 are not currently supported.'
    sys.exit(1)

entropy = args.n  *math.log(len(args.charset), 2) 

print 'Generating password with %s bits of entropy' % entropy

user_id = raw_input('user id: ')
master_pw = getpass.getpass('password: ')

pw = gen_password(master_pw, user_id)

print pw
