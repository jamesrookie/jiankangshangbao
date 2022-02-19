# -*- coding:utf-8 -*-
import base64
import binascii
import random
import string

from Crypto.Cipher import AES
from Crypto.Util import Counter


def int_of_string(s):
    return int(binascii.hexlify(s), 16)


# base64转hex
def b64_to_hex(b64_str):
    return base64.b64decode(b64_str).hex()


# 获取随机字符串
# ISO10126Padding 填充
# 在明文块末尾补足相应数量的字节，最后一个字符值等于缺少的字符数，其他字符填充随机数
def get_random_string(n):
    x = string.printable
    salt = ''
    for i in range(n):
        salt += random.choice(x)
    return salt


class AESData:
    encrypt_dict = {"CBC": AES.MODE_CBC, "ECB": AES.MODE_ECB, "CTR": AES.MODE_CTR, "OFB": AES.MODE_OFB,
                    "CFB": AES.MODE_CFB}

    def __init__(self, key, iv, blocksize):
        self.key = key  # 初始化密钥
        self.iv = iv  # 初始化偏移量
        self.length = AES.block_size  # 初始化数据块大小,默认16

        # 截断函数，去除填充的字符
        self.unpad = lambda data: data[0:-ord(data[-1])]

    def pad(self, text, pad_method):  # pad_method可以取两个值:0和1。0代表zeropadding,1代表pkcs5padding和pkcs7padding
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = ''
        if pad_method == 1:
            entext = text + (chr(add) * add)
        elif pad_method == 0:
            entext = text + '\0' * add
        elif pad_method == 2:
            # print(add)
            if count % self.length == 0:
                entext = text
            else:
                entext = text + '\0' * add
        elif pad_method == 3:
            entext = text + get_random_string(add - 1) + chr(add)
        elif pad_method == 4:
            entext = text + '\0' * (add - 1) + chr(add)
        return entext

    def encrypt_(self, encrData, padding, encrypt_method):  # 加密函数

        pad_method = -1
        if padding == "zeropadding":
            pad_method = 0
        elif padding == "pkcs5padding" or padding == "pkcs7padding":  # 后面的padding==一定不能省略
            pad_method = 1
        elif padding == 'nopadding':
            pad_method = 2
        elif padding == 'iso10126padding':
            pad_method = 3
        elif padding == 'ansix923padding':
            pad_method = 4
        if encrypt_method == "ECB":
            aes = AES.new(self.key, AESData.encrypt_dict[encrypt_method])  # ECB模式不需要iv偏移量
        elif encrypt_method == "CTR":
            ctr = Counter.new(128, initial_value=int_of_string(self.iv))
            aes = AES.new(self.key, AESData.encrypt_dict[encrypt_method], counter=ctr)
        else:
            aes = AES.new(self.key, AESData.encrypt_dict[encrypt_method], self.iv)  # 初始化AES,CBC模式的实例
        res = aes.encrypt(self.pad(encrData, pad_method).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt_(self, decrData, padding, encrypt_method):  # 解密函数
        if encrypt_method == "ECB":
            aes = AES.new(self.key, AESData.encrypt_dict[encrypt_method])  # ECB模式不需要iv偏移量
        elif encrypt_method == "CTR":
            ctr = Counter.new(128, initial_value=int_of_string(self.iv))
            aes = AES.new(self.key, AESData.encrypt_dict[encrypt_method], counter=ctr)
        else:
            aes = AES.new(self.key, AESData.encrypt_dict[encrypt_method], self.iv)  # 初始化AES,CBC模式的实例
        res = base64.decodebytes(decrData.encode("utf8"))
        # print(type(decrData))   #<class 'bytes'>
        # res=decrData
        msg = aes.decrypt(res).decode("utf8")
        if padding == "zeropadding" or padding == "nopadding":
            return msg.rstrip("\0")
        else:
            return self.unpad(msg)


def aes_encrypt_jiekou(origin_str, mode, padding, block_size, key, iv, output):
    enc = AESData(key.encode(), iv.encode(), block_size)
    encrypted = enc.encrypt_(origin_str, padding, mode)
    if output == "base64":
        return encrypted
    elif output == "hex":
        return b64_to_hex(encrypted)


def aes_decrypt_jiekou(encrypted, mode, padding, block_size, key, iv):
    enc = AESData(key.encode(), iv.encode(), block_size)
    decrypted = enc.decrypt_(encrypted, padding, mode)
    return decrypted

# result=aes_encrypt_jiekou("12345","ECB","pkcs5padding",128,"1234567812345678","1234567812345678","base64")
# print(result)
