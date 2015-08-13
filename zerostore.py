import base64
import getpass
import hashlib
import hmac
import pyperclip
import scrypt
import time

def gen_password(master_pw, user_id):
    hmac_key = scrypt.hash(master_pw, 'zerostore-salt'+user_id, N=16384, r=8, p=1, buflen=64)
    digest = hmac.HMAC(hmac_key, user_id, hashlib.sha256).digest()
    return base64.b64encode(digest[:16])

user_id = raw_input('user id: ')
master_pw = getpass.getpass('password: ')

pw = gen_password(master_pw, user_id)

pyperclip.copy(pw)
print 'Password copied to clipboard.'
time.sleep(10)
pyperclip.copy('[cleared]')
print 'Clipboard cleared.'
