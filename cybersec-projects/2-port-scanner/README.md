# 🔍 Python Port Scanner

A fast, multi-threaded TCP port scanner with service detection and optional banner grabbing. Built for learning network security concepts.

## ⚠️ Legal Disclaimer

> Only use this tool on systems **you own** or have **explicit written permission** to test. Unauthorized port scanning is illegal in many countries.

## Features

- ✅ Multi-threaded scanning (configurable threads)
- ✅ Service name detection for common ports
- ✅ Optional banner grabbing for service fingerprinting
- ✅ Quick scan mode for common ports only
- ✅ Hostname resolution
- ✅ Clean summary report

## Installation

No external libraries required — uses Python standard library only.

```bash
python port_scanner.py --help
```

## Usage

```bash
# Scan ports 1-1024 on localhost
python port_scanner.py 127.0.0.1

# Scan specific port range
python port_scanner.py 192.168.1.1 -s 1 -e 65535

# Scan only common ports with banner grabbing
python port_scanner.py 127.0.0.1 --common --banners

# Custom thread count and timeout
python port_scanner.py 192.168.1.1 -t 200 --timeout 0.5
```

## Example Output

```
🎯 Target   : 127.0.0.1
📡 Ports    : 1 - 1024
🧵 Threads  : 100

  [OPEN] Port 22     | SSH             | OpenSSH 8.9
  [OPEN] Port 80     | HTTP
  [OPEN] Port 443    | HTTPS

✅ Scan complete
📊 Open ports found: 3
```

## Concepts Demonstrated

- TCP socket programming
- Multi-threading with queue management
- Network service fingerprinting
- Banner grabbing
- CLI argument parsing with argparse
