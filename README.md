# TCP / Network Connectivity Monitor

A lightweight Python script that continuously monitors TCP connectivity, DNS resolution, and HTTP(S) availability for a list of sites.  
It is designed to detect **intermittent ISP issues, DNS delays, or web timeouts** by logging per-attempt results and generating **15-minute summary statistics**.

---

## ✨ Features
- 🔗 **TCP connectivity tests** (default port 443)
- 🧪 Multiple retries per site per round (default: 3 attempts)
- ⏱️ Logs connection latency (ms) for successful attempts
- 📊 **15-minute summary statistics**:
  - Total attempts
  - Success vs failure counts
  - Average, minimum, and maximum latency
- 📝 Continuous per-attempt logging
- 🛠️ Easily configurable (sites, ports, retries, log paths)

---

## 📂 Files
- `tcp_monitor.py` → The main monitoring script
- `connection_log.txt` → Detailed per-attempt logs
- `connection_summary.txt` → 15-minute rollup summaries

---

## 🚀 Installation

### Requirements
- Python 3.6+
