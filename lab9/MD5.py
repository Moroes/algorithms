# Little Endian

from calendar import c
from collections.abc import ByteString 
import hashlib
from random import choice
from string import ascii_uppercase
from collections import Counter


# from table import K, shiftamount
# from tool import *
import struct
from time import time

# reference
# https://cs.indstate.edu/~fsagar/doc/paper.pdf


#Constants

BITPERBYTE = 8
GROUPLEN = 512  # bits
GROUPREMAIN = 448  # bits
WORDLEN = 32  # bits
WORDNUM = 16  # 16 words in one group
PADDINGLEN = GROUPLEN - GROUPREMAIN
OPERATIONNUM = 64  # 64 operations
OPERATIONROUND = 4  # 4 rounds


import math
import doctest

OPERATION_NUM = 64

def calculate_K_table():
    """
    >>> K_table = calculate_K_table()
    >>> K == K_table
    True
    """
    K = [0 for _ in range(OPERATION_NUM)]
    for i in range(OPERATION_NUM):
        K[i] = int(abs(math.sin(i + 1)) * (2**32))
    return K


K = [ 
    0xd76aa478,
    0xe8c7b756,
    0x242070db,
    0xc1bdceee,
    0xf57c0faf,
    0x4787c62a,
    0xa8304613,
    0xfd469501,
    0x698098d8,
    0x8b44f7af,
    0xffff5bb1,
    0x895cd7be,
    0x6b901122,
    0xfd987193,
    0xa679438e,
    0x49b40821,
    0xf61e2562,
    0xc040b340,
    0x265e5a51,
    0xe9b6c7aa,
    0xd62f105d,
    0x02441453,
    0xd8a1e681,
    0xe7d3fbc8,
    0x21e1cde6,
    0xc33707d6,
    0xf4d50d87,
    0x455a14ed,
    0xa9e3e905,
    0xfcefa3f8,
    0x676f02d9,
    0x8d2a4c8a,
    0xfffa3942,
    0x8771f681,
    0x6d9d6122,
    0xfde5380c,
    0xa4beea44,
    0x4bdecfa9,
    0xf6bb4b60,
    0xbebfbc70,
    0x289b7ec6,
    0xeaa127fa,
    0xd4ef3085,
    0x04881d05,
    0xd9d4d039,
    0xe6db99e5,
    0x1fa27cf8,
    0xc4ac5665,
    0xf4292244,
    0x432aff97,
    0xab9423a7,
    0xfc93a039,
    0x655b59c3,
    0x8f0ccc92,
    0xffeff47d,
    0x85845dd1,
    0x6fa87e4f,
    0xfe2ce6e0,
    0xa3014314,
    0x4e0811a1,
    0xf7537e82,
    0xbd3af235,
    0x2ad7d2bb,
    0xeb86d391,
]

shiftamount = [
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    7,
    12,
    17,
    22,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    5,
    9,
    14,
    20,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    4,
    11,
    16,
    23,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21,
    6,
    10,
    15,
    21
]


def aux_f(b, c, d):
    return (b & c) | ((~b) & d)

def aux_g(b, c, d):
    return (b & d) | (c & (~d))

def aux_h(b, c, d):
    return b ^ c ^ d

def aux_i(b, c, d):
    return c ^ (b | (~d))

def reverse_int(integer, bytenum=4):
    """
    Reverse the byte order of integer 
    >>> a = 1 + 2**(4 * 8)  # 4-byte integer plus one
    >>> hex(a)
    '0x100000001'
    >>> a = reverse_int(a, bytenum=4)
    >>> hex(a)
    '0x01000010'
    """
    # assert isinstance(integer, Integral)
    fmt = {
        4: "I", # 4-byte unsigned int
        8: "Q", # 8-byte unsigned int
    }[bytenum]
    return struct.unpack(f">{fmt}", struct.pack(f"<{fmt}", integer))[0]

def modadd(a, *args):
    for v in args:
        a += v
        a %= (2**32)
    return a


def leftrotate(obj, length):
    return (obj << length) | (obj >> (32 - length))


def bit_fetch(num):
    return (1 << num) - 1


def count_bit(obj):
    num = 0
    while obj:
        obj >>= 1
        num += 1
    return num

def md5_padding(obj, nbits):
    """
    >>> grouplen = 512
    >>> groupremain = 448
    >>> a = 0b11000
    >>> a <<= 1
    >>> bin(a)
    '0b110000'
    >>> a ^= 1
    >>> bin(a)
    '0b110001'
    >>> a <<= (groupremain - count_bit(a)) - 1
    >>> bin(a)
    '0b110001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    """
    obj = (obj << 1) ^ 1
    obj = (obj << (nbits - 1))
    return obj


def md5_prepare(s):
    assert isinstance(s, ByteString)
    total_bitlen = bit_len = len(s) * BITPERBYTE
    remainder = bit_len % GROUPLEN
    s = int.from_bytes(s, "big")
    padding_len = (GROUPREMAIN - remainder) % GROUPLEN
    if padding_len == 0:
        padding_len = GROUPLEN
    padded_s = md5_padding(s, padding_len) # Добавляем 1 и нули (выравнивание)
    bit_len %= 2**64  # 64-bits length
    bit_len = reverse_int(bit_len, bytenum=8)
    padded_s = (padded_s << PADDINGLEN) + bit_len # Добавляем длину сообщения в порядке little-endian
    total_bitlen += (padding_len + 64)
    return padded_s, total_bitlen


def md5_group(s, total_bitlen):
    """
    Split message s (after padded) into several 512-bits group, then split each group into 16 words of 32-bits
    """
    group_num, rem = divmod(total_bitlen, GROUPLEN)
    if rem == 0:
        group_num -= 1
    group_list = [[0 for _ in range(WORDNUM)] for __ in range(group_num + 1)]
    group_fetch_int = bit_fetch(GROUPLEN)
    word_fetch_int = bit_fetch(WORDLEN)
    ind = 0
    while s:
        g = s & group_fetch_int
        word_ind = 0
        while g:
            word = g & word_fetch_int
            group_list[group_num - ind][WORDNUM - word_ind - 1] = reverse_int(word, bytenum=4)
            g >>= WORDLEN
            word_ind += 1
        s >>= GROUPLEN
        ind += 1
    return group_list, ind


def md5(group_list):
    AA = A = 0x67452301
    BB = B = 0xEFCDAB89
    CC = C = 0x98BADCFE
    DD = D = 0x10325476

    for group in group_list:
        A = AA
        B = BB
        C = CC
        D = DD
        for ind in range(OPERATIONNUM):
            if ind <= 15:
                F = aux_f(B, C, D)
                g = ind
            elif 16 <= ind <= 31:
                F = aux_g(B, C, D)
                g = (5 * ind + 1) % 16
            elif 32 <= ind <= 47:
                F = aux_h(B, C, D)
                g = (3 * ind + 5) % 16
            elif 48 <= ind <= 63:
                F = aux_i(B, C, D)
                g = (7 * ind) % 16
            dtemp = D
            D = C
            C = B
            B = modadd(B, leftrotate(modadd(A, F, K[ind], group[g]), shiftamount[ind]))
            A = dtemp
        AA = modadd(AA, A)
        BB = modadd(BB, B)
        CC = modadd(CC, C)
        DD = modadd(DD, D)
    output_list = [AA, BB, CC, DD]
    # Reverse each word
    for ind, word in enumerate(output_list):
        output_list[ind] = reverse_int(word)
    AA, BB, CC, DD = output_list
    return f"{AA:=08x}{BB:=08x}{CC:=08x}{DD:=08x}"  # Append zero before each byte to 8 characters
 
def analys_str():
    c = 1
    letters = 1
    count = {}
    for i in range(5):
        for j in range(1000):
            word1 = 'a' * (128-letters) + (f'{j}'*letters)
            word2 = 'a' * (128-letters) + ('s'*letters)
            word1 = hsh(word1)
            word2 = hsh(word2)
            for k in range(len(word1)):
                if word1[k] == word2[k]:
                    for k2 in range(k, len(word1)):
                        if word1[k2] == word2[k2]:
                            c += 1
                        else:
                            if count.get(c) is None:
                                count[c] = 0
                            else:
                                count[c] += 1
                                c = 1
                                break
        letters *= 2
    print(count)

def analys_collision():
    hash = []
    count = {}
    for i in range(2, 6):
        N = pow(10, i)
        for j in range(N):
            hash.append(''.join(choice(ascii_uppercase) for i in range(256)))
        res = [k for k,v in Counter(hash).items() if v>1]
    print(res)

def analys_time():
    length = 64
    times = {}
    for i in range(8):
        start_time = time()
        for j in range(1000):
            res = hsh(''.join(choice(ascii_uppercase) for i in range(length)))
        times[length] = time() - start_time
        length *= 2
    print(times)

def hsh(msg):
    msg_enc = msg.encode()
    prepared_msg, total_bitlen = md5_prepare(msg_enc)
    groups, group_num = md5_group(prepared_msg, total_bitlen)
    md5_msg = md5(groups)
    # print(md5_msg)
    return md5_msg

def main():
    analys_str()
    analys_collision()
    analys_time()

# main()
m = "asd"
asnw1 = hashlib.md5(m.encode()).hexdigest()
answ2 = hsh(m)
print(asnw1)
print(answ2)