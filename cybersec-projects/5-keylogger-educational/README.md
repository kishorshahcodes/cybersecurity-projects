# ⌨️ Educational Keylogger

A **transparent, consent-based** keylogger built to understand how keystroke logging works — and why endpoint security tools exist to stop it.

## ⚠️ Legal & Ethical Disclaimer

> This tool is for **educational use only** on systems **you own**.
> Using a keylogger on someone else's computer **without consent** is illegal under laws including the Computer Fraud and Abuse Act (CFAA), UK Computer Misuse Act, and similar laws worldwide.

## What Makes This "Educational"

Unlike real malware keyloggers, this tool is intentionally:
- ✅ Transparent (visible process, obvious log file name)
- ✅ Consent-gated (requires typing "I AGREE" before starting)
- ✅ Local only (no network transmission, no email exfiltration)
- ✅ Easily stoppable (ESC key or Ctrl+C)
- ✅ Clearly documented

## Installation

```bash
pip install pynput
```

## Usage

```bash
python keylogger.py
```

You'll be prompted to confirm consent before it starts.

## Example Log Output

```
=== Educational Keylogger Session ===
Started: 2024-01-15T10:30:00

Hello [SPACE] World[ENTER]
[BACKSPACE]testing[ENTER]
```

## What Real Malicious Keyloggers Do Differently

| Feature | This Tool | Real Malware |
|---------|-----------|--------------|
| Visible process | ✅ Yes | ❌ Hidden |
| Network exfiltration | ❌ None | ✅ Emails logs |
| Persistence | ❌ None | ✅ Startup entries |
| Consent required | ✅ Yes | ❌ No |
| Detectable by AV | ✅ Yes | Often no |

## How to Protect Against Real Keyloggers

- Keep OS and antivirus updated
- Use a password manager
- Enable 2FA on accounts
- Avoid installing untrusted software
- Use hardware security keys for critical accounts

## Concepts Demonstrated

- Keyboard event listening with `pynput`
- Signal handling (Ctrl+C)
- Ethical security research practices
- Understanding threat actor techniques (for defense)
