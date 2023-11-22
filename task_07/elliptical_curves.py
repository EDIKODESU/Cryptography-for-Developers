from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import json
import random

class ECPoint:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

def base_point_g_get():
    curve = ec.SECP256R1() 
    private_key = ec.generate_private_key(curve, default_backend())
    public_key = private_key.public_key()
    
    x, y = public_key.public_numbers().x, public_key.public_numbers().y
    return ECPoint(x, y)

def ec_point_gen(x, y):
    return ECPoint(x, y)

def is_on_curve_check(a):
    curve = ec.SECP256R1()
    try:
        point = ec.EllipticCurvePublicNumbers(int(a.X), int(a.Y), curve).public_key(default_backend()).public_numbers()
        curve.verify(
            point, b"\x00", b"\x00", ec.ECDSA(hashes.SHA256())
        )
        return True
    except ValueError:
        return False


def add_ec_points(a, b):
    curve = ec.SECP256R1()  
    result = a.X + b.X, a.Y + b.Y
    return ECPoint(result[0], result[1])

def double_ec_points(a):
    curve = ec.SECP256R1()  
    result = a.X * 2, a.Y * 2
    # result = curve.double_point((a.X, a.Y))
    return ECPoint(result[0], result[1])

def scalar_mult(k, a):
    curve = ec.SECP256R1()  
    result = a.X * k, a.Y * k
    return ECPoint(result[0], result[1])

def ec_point_to_string(point):
    return json.dumps({"X": point.X, "Y": point.Y})

def string_to_ec_point(s):
    data = json.loads(s)
    return ECPoint(data["X"], data["Y"])

def print_ec_point(point):
    print(f"X: {point.X}\nY: {point.Y}")

def set_random(bit_length):
    return random.getrandbits(bit_length)

def is_equal(a, b):
    return a.X == b.X and a.Y == b.Y

# Example usage of wrapper functions
G = base_point_g_get()
k = set_random(256)
d = set_random(256)

# Check scalar mult
print("\nCheck scalar mult")
H1 = scalar_mult(d, G)
H2 = scalar_mult(k, H1)

H3 = scalar_mult(k, G)
H4 = scalar_mult(d, H3)

result = is_equal(H2, H4)
print("Correctness Check Result:", result)

# Check is_on_curve_check
# result_on_curve_G = is_on_curve_check(G)
# result_on_curve_H1 = is_on_curve_check(H1)
# result_on_curve_H2 = is_on_curve_check(H2)

# print("Is G on curve?", result_on_curve_G)
# print("Is H1 on curve?", result_on_curve_H1)
# print("Is H2 on curve?", result_on_curve_H2)

# Check ec_point_gen
print("\nCheck ec_point_gen")
P = ec_point_gen(123, 456)
result_on_curve_P = is_on_curve_check(P)
print_ec_point(P)
print("Is P on curve?", result_on_curve_P)

# Check add_ec_points
print("\nCheck add_ec_points")
Q = add_ec_points(G, P)
result_on_curve_Q = is_on_curve_check(Q)
print_ec_point(Q)
print("Is Q on curve?", result_on_curve_Q)

# Check double_ec_points
print("\nCheck double_ec_points")
R = double_ec_points(P)
result_on_curve_R = is_on_curve_check(R)
print_ec_point(R)
print("Is R on curve?", result_on_curve_R)

# Check ec_point_to_string
print("\nCheck ec_point_to_string")
string_representation_P = ec_point_to_string(P)
reconstructed_P = string_to_ec_point(string_representation_P)
result_string_conversion = is_equal(P, reconstructed_P)
print("String conversion result:", result_string_conversion)

# Check print_ec_point
print("\nCheck print_ec_point")
print("Printed point:")
print_ec_point(P)

