#!/usr/bin/env python3
import socket
import time
from datetime import datetime, timedelta

# Configuration
SITES = ["youtube.com", "microsoft.com"]
PORT = 443
TIMEOUT = 2       # seconds per TCP attempt
RETRIES = 3       # attempts per site each round
SLEEP = 5         # seconds between rounds
SUMMARY_INTERVAL = 15 * 60  # 15 minutes in seconds
LOGFILE = "connection_log.txt"  # per-attempt log
SUMMARYFILE = "connection_summary.txt"  # summary log

# Store stats for summary
stats = {site: [] for site in SITES}
last_summary_time = time.time()

def test_site(site):
    try:
        ip = socket.gethostbyname(site)
    except Exception:
        ip = None

    results = []
    for _ in range(RETRIES):
        try:
            start = time.time()
            sock = socket.create_connection((ip, PORT), timeout=TIMEOUT)
            latency = (time.time() - start) * 1000  
            sock.close()
            results.append((True, latency))
        except socket.timeout:
            results.append((False, None))
        except Exception:
            results.append((False, None))
    return ip, results

def log_results(site, ip, results):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success_count = sum(1 for r in results if r[0])
    line = f"{timestamp} {site} ({ip if ip else 'N/A'}): {success_count}/{len(results)} success"
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")
        for idx, (success, latency) in enumerate(results, start=1):
            detail = f"Attempt {idx}: {'SUCCESS' if success else 'FAIL/TIMEOUT'}"
            if latency is not None:
                detail += f", {latency:.1f} ms"
            f.write("  " + detail + "\n")
        f.write("\n")
    # Store for summary
    stats[site].extend(results)

def generate_summary():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_lines = [f"{timestamp} --- 15 Minute Summary ---"]
    for site, results in stats.items():
        total = len(results)
        successes = [r[1] for r in results if r[0]]
        failures = total - len(successes)
        avg_latency = sum(successes)/len(successes) if successes else None
        min_latency = min(successes) if successes else None
        max_latency = max(successes) if successes else None
        line = f"{site}: {len(successes)}/{total} success"
        if avg_latency is not None:
            line += f", avg {avg_latency:.1f} ms, min {min_latency:.1f} ms, max {max_latency:.1f} ms"
        else:
            line += ", no successful connections"
        summary_lines.append(line)
        # Reset stats for next interval
        stats[site] = []
    summary_lines.append("\n")
    print("\n".join(summary_lines))
    with open(SUMMARYFILE, "a") as f:
        f.write("\n".join(summary_lines) + "\n")

if __name__ == "__main__":
    while True:
        for site in SITES:
            ip, results = test_site(site)
            log_results(site, ip, results)
        time.sleep(SLEEP)
        if time.time() - last_summary_time >= SUMMARY_INTERVAL:
            generate_summary()
            last_summary_time = time.time()
