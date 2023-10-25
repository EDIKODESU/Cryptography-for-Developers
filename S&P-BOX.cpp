#include <vector>
#include <iostream>
#include <cstdint>

using namespace std;

//constant table s-box
const vector<vector<uint8_t>> SBox = {
    {0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76},
    {0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0},
    {0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15},
    {0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75},
    {0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84},
    {0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF},
    {0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8},
    {0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2},
};

// Function to perform substitution using the S-Box
uint8_t SBoxEncrypt(uint8_t input) {
    uint8_t row = (input >> 4) & 0x0F;    // First 4 bits
    uint8_t col = input & 0x0F;          // Last 4 bits
    return SBox[row][col];
}

// Function to reverse the substitution done by the S-Box
uint8_t SBoxDecrypt(uint8_t input) {
    for (int row = 0; row < 16; row++) {
        for (int col = 0; col < 16; col++) {
            if (SBox[row][col] == input) {
                return (row << 4) | col;
            }
        }
    }
    return 0xFF; 
}

// Function to perform bit permutation
uint8_t PBox(uint8_t input) {
    uint8_t output_data = 0;
    for (int i = 0; i < 8; i++) {
        output_data |= ((input >> i) & 1) << (7 - i);
    }
    return output_data;
}

// Function to run tests on S-Box and P-Box functions
void runTests() {
    // Test of the SBoxEncrypt function
    uint8_t plaintext_S = 0x53;
    uint8_t encrypted = SBoxEncrypt(plaintext_S);
    uint8_t decrypted = SBoxDecrypt(encrypted);

    cout << "S-Box Test:" << endl;
    cout << "Plaintext: " << hex << (int)plaintext_S << endl;
    cout << "Encrypted: " << hex << (int)encrypted << endl;
    cout << "Decrypted: " << hex << (int)decrypted << endl;
    cout << (plaintext_S == decrypted ? "S-Box Encryption Test Passed" : "S-Box Encryption Test Failed") << endl;

    // PBox function test
    uint8_t plaintext_P = 0x55;
    uint8_t permuted = PBox(plaintext_P);
    uint8_t decrypted_P = PBox(permuted);

    cout << "P-Box Test:" << endl;
    cout << "Plaintext: " << hex << (int)plaintext_P << endl;
    cout << "Permuted: " << hex << (int)permuted << endl;
    cout << "Decrypted: " << hex << (int)decrypted_P << endl;
    cout << (plaintext_P == decrypted_P ? "P-Box Test Passed" : "P-Box Test Failed") << endl;
}

int main() {
    runTests();
    return 0;
}
