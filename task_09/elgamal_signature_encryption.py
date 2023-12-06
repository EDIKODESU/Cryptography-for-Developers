import random
import hashlib
import math
from sympy import isprime

def generate_prime(bits):
    while True:
        candidate = random.SystemRandom().getrandbits(bits) | 1  # Ensure odd
        if isprime(candidate):
            return candidate

def is_quadratic_residue(n, p):
    # Check if n is a quadratic residue modulo p
    return pow(n, (p - 1) // 2, p) == 1

def find_primitive_root(p):
    if not isprime(p):
        raise ValueError("Input must be a prime number.")

    # Try random values until a primitive root is found
    while True:
        candidate = random.randint(2, p - 2)
        if not is_quadratic_residue(candidate, p):
            return candidate

def generate_keys(p, g):
    while True:
        a = random.randint(1, p - 1)  # Private key (1 <= a <= p-2)
        if math.gcd(a, p - 1) == 1:
            break

    b = pow(g, a, p)  # Public key
    return a, b

def sign_message(message, p, g, a):
    while True:
        k = random.randint(1, p - 2)
        gcd_val, _, k_inv = extended_gcd(k, p - 1)
        if gcd_val == 1 and k_inv is not None and k_inv > 0:
            h = int(hashlib.sha256(message.encode()).hexdigest(), 16)
            r = pow(g, k, p)

            # Ensure s has a modular inverse
            try:
                s_candidate = (k_inv * (h + a * r)) % (p - 1)
                s = mod_inverse(s_candidate, p - 1)
                if s is not None:
                    return r, s
            except ValueError:
                # Skip problematic cases and try a new random k
                continue

def extended_gcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None  # The modular inverse does not exist
    return x % m

def verify_signature(message, r, s, p, g, b):
    h = int(hashlib.sha256(message.encode()).hexdigest(), 16)

    if not (0 < r < p and 0 < s < p - 1):
        return False  # Invalid r or s values

    if s == 1:
        return False  # Invalid s value

    try:
        w = mod_inverse(s, p - 1)
        u1 = (h * w) % (p - 1)
        u2 = (r * w) % (p - 1)
        v = (pow(g, u1, p) * pow(b, u2, p)) % p
    except ValueError:
        return False  # Handle exceptions gracefully

    if v == r:
        return True
    else:
        return False  # Invalid signature

def encrypt(message, p, g, b):
    k = random.randint(1, p - 2)
    x = pow(g, k, p)
    
    if isinstance(message, str):
        m = int.from_bytes(message.encode(), 'big') % p
    elif isinstance(message, int):
        m = message % p
    else:
        raise ValueError("Unsupported message type")

    y = (pow(b, k, p) * m) % p
    return x, y

def decrypt(ciphertext, a, p):
    x, y = ciphertext
    s = pow(x, a, p)
    m = (y * pow(s, -1, p)) % p
    return m

def test_crypto_operations():
    p = generate_prime(2048)
    print("Prime:", p)
    g = find_primitive_root(p)
    print("Primitive Root:", g)
    private_key, public_key = generate_keys(p, g)

    message_1 = "Hello, World!"
    message_2 = 42

    # Digital Signature Test
    signature = sign_message(message_1, p, g, private_key)
    verified = verify_signature(message_1, *signature, p, g, public_key)

    # Encryption and Decryption Test
    ciphertext = encrypt(message_2, p, g, public_key)
    decrypted_message = decrypt(ciphertext, private_key, p)

    print("Original Message 1:", message_1)
    print("Signature (r, s):", signature)
    print("Signature Verified:", verified)

    print("\nOriginal Message 2:", message_2)
    print("Ciphertext (x, y):", ciphertext)
    print("Decrypted Message:", decrypted_message)

test_crypto_operations()
