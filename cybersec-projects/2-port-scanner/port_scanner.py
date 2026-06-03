"""
Port Scanner
Author: [Your Name]
Description: A multi-threaded TCP port scanner with service detection and banner grabbing.
             For educational and authorized network testing purposes only.
"""

import socket
import threading
import queue
import sys
import argparse
from datetime import datetime


# Common ports and their services
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB"
}

open_ports = []
lock = threading.Lock()


def grab_banner(ip, port, timeout=2):
    """Try to grab a service banner from an open port."""
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((ip, port))
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        return banner[:80] if banner else None
    except Exception:
        return None


def scan_port(ip, port, timeout, grab_banners):
    """Attempt to connect to a single port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))
        s.close()

        if result == 0:
            service = COMMON_SERVICES.get(port, "Unknown")
            banner = grab_banner(ip, port) if grab_banners else None

            with lock:
                open_ports.append((port, service, banner))
                status = f"  [OPEN] Port {port:<6} | {service:<15}"
                if banner:
                    status += f" | Banner: {banner}"
                print(status)
    except socket.error:
        pass


def worker(ip, timeout, grab_banners, q):
    """Thread worker: pull ports from queue and scan them."""
    while not q.empty():
        port = q.get()
        scan_port(ip, port, timeout, grab_banners)
        q.task_done()


def resolve_host(target):
    """Resolve hostname to IP address."""
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"❌ Could not resolve host: {target}")
        sys.exit(1)


def print_banner():
    print("""
╔══════════════════════════════════════╗
║        🔍 Python Port Scanner        ║
║   For authorized testing only        ║
╚══════════════════════════════════════╝
    """)


def scan(target, start_port, end_port, threads, timeout, grab_banners):
    print_banner()

    ip = resolve_host(target)
    print(f"🎯 Target   : {target} ({ip})")
    print(f"📡 Ports    : {start_port} - {end_port}")
    print(f"🧵 Threads  : {threads}")
    print(f"⏱  Timeout  : {timeout}s")
    print(f"🚀 Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 55)
    print(f"\n{'Port':<10} {'Service':<15} {'Banner'}")
    print("-" * 55)

    q = queue.Queue()
    for port in range(start_port, end_port + 1):
        q.put(port)

    thread_list = []
    for _ in range(min(threads, end_port - start_port + 1)):
        t = threading.Thread(target=worker, args=(ip, timeout, grab_banners, q))
        t.daemon = True
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    print("\n" + "=" * 55)
    print(f"✅ Scan complete at {datetime.now().strftime('%H:%M:%S')}")
    print(f"📊 Open ports found: {len(open_ports)}")

    if open_ports:
        print("\n📋 Summary:")
        for port, service, banner in sorted(open_ports):
            print(f"   Port {port} ({service})" + (f" — {banner}" if banner else ""))
    print("=" * 55 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="🔍 Python Port Scanner - For authorized use only"
    )
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds (default: 1.0)")
    parser.add_argument("--banners", action="store_true", help="Attempt to grab service banners")
    parser.add_argument("--common", action="store_true", help="Scan only common ports")

    args = parser.parse_args()

    if args.common:
        ports = list(COMMON_SERVICES.keys())
        print(f"\n⚡ Scanning {len(ports)} common ports...")
        q = queue.Queue()
        for port in ports:
            q.put(port)
        ip = resolve_host(args.target)
        for _ in range(min(args.threads, len(ports))):
            t = threading.Thread(target=worker, args=(ip, args.timeout, args.banners, q))
            t.daemon = True
            t.start()
        q.join()
        print(f"\n✅ Found {len(open_ports)} open ports")
    else:
        scan(args.target, args.start, args.end, args.threads, args.timeout, args.banners)


if __name__ == "__main__":
    print("\n⚠️  WARNING: Only scan systems you own or have explicit permission to test.")
    print("   Unauthorized port scanning may be illegal in your jurisdiction.\n")
    main()
