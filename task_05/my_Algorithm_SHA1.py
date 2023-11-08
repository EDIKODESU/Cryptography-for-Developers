import hashlib
import timeit
import struct

# Функції SHA-1
def left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def sha1_padding(message):
    ml = len(message) * 8
    message += b'\x80'
    while (len(message) + 8) % 64 != 0:
        message += b'\x00'
    message += struct.pack('>Q', ml)
    return message

def sha1(message):
    message = sha1_padding(message)
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        words = list(struct.unpack('>16I', chunk))
        for j in range(16, 80):
            words.append(left_rotate(words[j-3] ^ words[j-8] ^ words[j-14] ^ words[j-16], 1))

        a, b, c, d, e = h0, h1, h2, h3, h4

        for j in range(80):
            if j <= 19:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            elif j <= 39:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            elif j <= 59:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6

            temp = (left_rotate(a, 5) + f + e + k + words[j]) & 0xFFFFFFFF
            e, d, c, b, a = d, c, left_rotate(b, 30), a, temp

        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    return struct.pack('>5I', h0, h1, h2, h3, h4)

# Тестові повідомлення 
messages = [b'Hello, World!', b'Ediko Hlinystyi', b'12345', b'Distributed Lab']

for message in messages:
    # Моя реалізація SHA-1
    custom_hash = sha1(message).hex()

    # Бібліотечна реалізація SHA-1
    hashlib_sha1 = hashlib.sha1(message).digest().hex()

    print(f'Custom Hash: {custom_hash}')
    print(f'Hashlib Hash: {hashlib_sha1}')

    # Порівняння результатів
    if custom_hash == hashlib_sha1:
        print(f'SHA-1 Hash for message "{message.decode()}": MATCHES')
    else:
        print(f'SHA-1 Hash for message "{message.decode()}": DOES NOT MATCH')

    # Перевірка швидкості виконання функцій
    time_custom_hash = timeit.timeit(lambda: sha1(message), number = 1000)
    time_hashlib_sha1 = timeit.timeit(lambda: hashlib.sha1(message).hexdigest(), number = 1000)

    print(f'Time Custom Hash: {time_custom_hash}')
    print(f'Time Hashlib Hash: {time_hashlib_sha1}\n')

