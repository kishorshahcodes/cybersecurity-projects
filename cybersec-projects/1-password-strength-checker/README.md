# 🔐 Password Strength Analyzer & Breach Checker

A Python tool that analyzes password strength and checks if your password has been exposed in known data breaches using the [HaveIBeenPwned](https://haveibeenpwned.com/) API.

## Features

- ✅ Checks password length, character variety, entropy
- ✅ Detects common patterns and repeated characters
- ✅ Calculates password entropy (in bits)
- ✅ Checks against 600M+ breached passwords via HIBP API
- ✅ **Privacy-safe**: Uses k-anonymity — your actual password is never sent

## How It Works (k-Anonymity)

1. Your password is hashed with SHA-1 locally
2. Only the **first 5 characters** of the hash are sent to the API
3. The API returns all matching hash suffixes
4. Your device checks locally if your full hash is in the list

Your actual password never leaves your machine. ✅

## Installation

```bash
pip install requests
```

## Usage

```bash
python password_checker.py
```

## Example Output

```
📊 Strength Rating : 🟢 STRONG
📐 Entropy         : 52.44 bits
📏 Length          : 12 characters

📋 Detailed Feedback:
   ✅ Good length
   ✅ Contains lowercase letters
   ✅ Contains uppercase letters
   ✅ Contains numbers
   ✅ Contains special characters

🌐 Checking breach databases...
   ✅ Good news! This password was NOT found in known breach databases.
```

## Concepts Demonstrated

- SHA-1 hashing
- API integration
- k-anonymity privacy model
- Regex pattern matching
- Password entropy calculation

## Disclaimer

This tool is for **educational purposes**. Always use a reputable password manager for real-world use.
