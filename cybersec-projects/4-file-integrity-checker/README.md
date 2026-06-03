# 🛡️ File Integrity Checker

A Python tool that monitors files and directories for unauthorized changes using SHA-256 cryptographic hashing. Similar in concept to tools like Tripwire or AIDE used in real-world security operations.

## Features

- ✅ SHA-256 hash-based file integrity verification
- ✅ Detects modified, deleted, and newly added files
- ✅ Records file size and modification timestamps
- ✅ JSON-based baseline storage
- ✅ Directory-wide recursive scanning
- ✅ Single file hash utility

## Installation

No external libraries required.

## Usage

### Step 1: Create a baseline

```bash
python file_integrity_checker.py /path/to/monitor --create
```

### Step 2: Verify integrity later

```bash
python file_integrity_checker.py /path/to/monitor --verify
```

### Hash a single file

```bash
python file_integrity_checker.py . --hash-file myfile.txt
```

## Example Output

```
📊 Integrity Report — 2024-01-15 10:30:00
═══════════════════════════════════════════════════════

⚠️  MODIFIED FILES (1):
   📝 config/settings.py
      Hash : a3f8b2c1d4e5... → 9x2k1m3n5p7q...
      Time : 2024-01-14 → 2024-01-15

🗑️  DELETED FILES (1):
   ❌ logs/debug.log

🆕 NEW FILES (1):
   ➕ uploads/shell.php

🚨 Total changes detected: 3
```

## Real-World Application

This type of tool is used in:
- **Intrusion Detection Systems (IDS)** to detect if an attacker modified system files
- **Software supply chain security** to verify package integrity
- **Compliance** (PCI-DSS, HIPAA) requires file integrity monitoring

## Concepts Demonstrated

- SHA-256 cryptographic hashing
- File system traversal with `pathlib`
- JSON data serialization
- Change detection algorithms
- Security baseline methodology
