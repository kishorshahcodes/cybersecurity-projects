# 🔒 Cryptography Tool

An interactive Python tool implementing classic and fundamental cipher techniques to learn cryptography from the ground up.

## Ciphers Implemented

| Cipher | Type | Description |
|--------|------|-------------|
| Caesar | Substitution | Shifts alphabet by N positions |
| ROT13 | Substitution | Caesar with fixed shift of 13 |
| Vigenère | Polyalphabetic | Uses a keyword for variable shifts |
| XOR | Bitwise | XORs each byte with a key |
| Base64 | Encoding | Binary-to-text encoding scheme |
| Caesar Brute Force | Cryptanalysis | Tries all 25 possible shifts |

## Installation

No external libraries required.

```bash
python encryption_tool.py
```

## Usage

Run the interactive menu:

```bash
python encryption_tool.py
```

## Example

```
Select option: 1
Enter text: Hello World
Enter shift: 3
(E)ncrypt or (D)ecrypt? E

✅ Encrypted: Khoor Zruog
```

## Concepts Demonstrated

- Classical cryptography (Caesar, Vigenère)
- XOR bitwise operations
- Base64 encoding/decoding
- Brute-force cryptanalysis
- Polyalphabetic substitution ciphers

## Educational Notes

- **Caesar Cipher**: Vulnerable to brute force (only 25 keys)
- **Vigenère**: Stronger but breakable with frequency analysis
- **XOR**: Fundamental to modern encryption (used in AES, stream ciphers)
- **Base64**: Not encryption — just encoding (easily reversible)

> 💡 These are classical ciphers. For real-world security, use AES-256, RSA, or established libraries like `cryptography` (Python).
