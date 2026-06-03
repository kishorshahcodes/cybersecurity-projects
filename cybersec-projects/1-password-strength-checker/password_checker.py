"""
Password Strength Analyzer & Breach Checker
Author: [Your Name]
Description: Analyzes password strength and checks if it has been exposed in known data breaches
             using the HaveIBeenPwned API (k-anonymity model - your password is never sent).
"""

import hashlib
import re
import requests
import math
import string


def calculate_entropy(password):
    """Calculate the entropy of a password in bits."""
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): charset += 32
    if charset == 0:
        return 0
    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)


def check_strength(password):
    """Check password strength and return a score and feedback."""
    score = 0
    feedback = []

    # Length checks
    if len(password) < 8:
        feedback.append("❌ Password is too short (minimum 8 characters)")
    elif len(password) < 12:
        feedback.append("⚠️  Password length is okay but 12+ characters is recommended")
        score += 1
    else:
        feedback.append("✅ Good length")
        score += 2

    # Character variety checks
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append("✅ Contains lowercase letters")
    else:
        feedback.append("❌ Missing lowercase letters")

    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append("✅ Contains uppercase letters")
    else:
        feedback.append("❌ Missing uppercase letters")

    if re.search(r'[0-9]', password):
        score += 1
        feedback.append("✅ Contains numbers")
    else:
        feedback.append("❌ Missing numbers")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 2
        feedback.append("✅ Contains special characters")
    else:
        feedback.append("❌ Missing special characters (!@#$%^&* etc.)")

    # Common patterns
    common_patterns = ['password', '123456', 'qwerty', 'abc123', 'letmein', 'admin']
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 2
        feedback.append("❌ Contains common password pattern")

    # Repeated characters
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        feedback.append("⚠️  Contains repeated characters (e.g. 'aaa')")

    # Strength rating
    entropy = calculate_entropy(password)
    if score <= 1:
        strength = "🔴 VERY WEAK"
    elif score <= 3:
        strength = "🟠 WEAK"
    elif score <= 5:
        strength = "🟡 MODERATE"
    elif score <= 6:
        strength = "🟢 STRONG"
    else:
        strength = "🟢 VERY STRONG"

    return strength, score, feedback, entropy


def check_pwned(password):
    """
    Check if password has been in a data breach using HaveIBeenPwned API.
    Uses k-anonymity: only the first 5 chars of SHA1 hash are sent.
    Your actual password is NEVER transmitted.
    """
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        response.raise_for_status()

        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return True, int(count)
        return False, 0

    except requests.RequestException as e:
        return None, f"Could not connect to breach database: {e}"


def display_results(password):
    """Display a full analysis of the password."""
    print("\n" + "="*55)
    print("       🔐 PASSWORD SECURITY ANALYZER")
    print("="*55)

    strength, score, feedback, entropy = check_strength(password)

    print(f"\n📊 Strength Rating : {strength}")
    print(f"📐 Entropy         : {entropy} bits")
    print(f"📏 Length          : {len(password)} characters")
    print(f"\n📋 Detailed Feedback:")
    for item in feedback:
        print(f"   {item}")

    print(f"\n🌐 Checking breach databases...")
    breached, count = check_pwned(password)

    if breached is None:
        print(f"   ⚠️  {count}")
    elif breached:
        print(f"   🚨 DANGER: This password has appeared {count:,} times in known data breaches!")
        print(f"   🔁 You should change this password immediately.")
    else:
        print(f"   ✅ Good news! This password was NOT found in known breach databases.")

    print("\n" + "="*55)
    print("💡 Tip: Use a password manager to generate & store strong passwords.")
    print("="*55 + "\n")


def main():
    print("\n🔐 Password Strength Analyzer & Breach Checker")
    print("   Your password is never stored or transmitted in plain text.\n")

    while True:
        import getpass
        password = getpass.getpass("Enter password to analyze (input hidden): ")
        if not password:
            print("No password entered. Exiting.")
            break

        display_results(password)

        again = input("Check another password? (y/n): ").strip().lower()
        if again != 'y':
            print("Stay secure! 🛡️")
            break


if __name__ == "__main__":
    main()
