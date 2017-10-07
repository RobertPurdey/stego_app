from tkinter import *
from gui import StegoGui
from Crypto.Cipher import AES
from Crypto.Hash import SHA
from hashlib import md5
from Crypto import Random
pword = "password"

msg = "Secret Message"
bin_filename = ''.join([bin(ord(ch))[2:].zfill(8) for ch in "BB"])
bin_filefrmt = [bin(ord(ch))[2:].zfill(8) for ch in "AA"]

print(str(bin_filename))