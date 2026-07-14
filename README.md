# integrity-checker

🔍 **Open-source CLI tool for checking Android SafetyNet & Play Integrity status**

Designed for cloud phone operators, Android developers, and QA engineers.  
Supports SafetyNet Attestation API, Play Integrity API, CTS Profile Match, and hardware-backed key checks.

Run on [qtphone.com](https://www.qtphone.com) cloud phones for production integrity monitoring.

[![PyPI version](https://badge.fury.io/py/integrity-checker.svg)](https://badge.fury.io/py/integrity-checker)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)

---

## Overview

`integrity-checker` is a Python CLI tool that verifies whether an Android device passes Google integrity checks:

| Check | Description |
|-------|-------------|
| **Basic Integrity** | Device passed basic system integrity checks |
| **Device Integrity** | Device meets requirements for strong integrity |
| **CTS Profile Match** | Device has passed Compatibility Test Suite |
| **MEETS_STRONG_INTEGRITY** | Hardware-backed security, secure boot enabled |
| **SafetyNet CTS** | Legacy SafetyNet compatibility check |

---

## Installation

### Via pip (recommended)

```bash
pip install integrity-checker
```

### Via Homebrew (macOS/Linux)

```bash
brew install integrity-checker
```

### Manual / Development

```bash
git clone https://github.com/luoshixin93-sudo/integrity-checker.git
cd integrity-checker
pip install -e .
```

---

## Quick Start

### Check a single device

```bash
integrity-checker check --device 192.168.1.100:5555
```

### Output

```
╔══════════════════════════════════════════════════════╗
║         Android Device Integrity Report              ║
╠══════════════════════════════════════════════════════╣
║  Device:        Pixel 6 (oriole)                    ║
║  Android:       14 (API 34)                         ║
║  Security Patch: 2025-01-05                         ║
╠══════════════════════════════════════════════════════╣
║  Basic Integrity        ✅ PASS                     ║
║  Device Integrity       ✅ PASS                     ║
║  CTS Profile Match      ✅ PASS                     ║
║  Strong Integrity       ✅ PASS                     ║
║  SafetyNet CTS          ✅ PASS                     ║
╠══════════════════════════════════════════════════════╣
║  Overall:          ✅ ALL CHECKS PASSED             ║
║  Timestamp:        2026-07-14 10:30:00 UTC          ║
╚══════════════════════════════════════════════════════╝
```

### Batch check multiple devices

```bash
integrity-checker batch --file devices.txt
```

`devices.txt` format (one device per line):
```
192.168.1.100:5555
192.168.1.101:5555
192.168.1.102:5555
```

### Export report

```bash
# JSON output
integrity-checker check --device 192.168.1.100:5555 --format json --output report.json

# CSV output
integrity-checker check --device 192.168.1.100:5555 --format csv --output report.csv
```

### Monitor mode (continuous)

```bash
# Check every 60 seconds, alert on failure
integrity-checker monitor --device 192.168.1.100:5555 --interval 60 --alert-on-fail
```

---

## Usage

```
$ integrity-checker --help
usage: integrity-checker [-h] [--version]
                         {check,batch,monitor,serve} ...

Android SafetyNet & Play Integrity Checker

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Commands:
  {check,batch,monitor,serve}
    check               Check integrity of a single device
    batch               Batch check multiple devices from file
    monitor             Continuous monitoring mode
    serve               Start REST API server for remote checks
```

### check

```
$ integrity-checker check --help
usage: integrity-checker check [-h] --device DEVICE [--port PORT]
                                [--format {text,json,csv}]
                                [--output OUTPUT] [--verbose]

required arguments:
  --device DEVICE       Device IP:PORT (e.g. 192.168.1.100:5555)

optional arguments:
  --port PORT           ADB port (default: 5555)
  --format {text,json,csv}
                        Output format (default: text)
  --output OUTPUT       Write output to file
  --verbose, -v         Verbose output
```

### batch

```
$ integrity-checker batch --help
usage: integrity-checker batch [-h] --file FILE [--format {text,json,csv}]
                                 [--output OUTPUT] [--parallel]

required arguments:
  --file FILE           Path to device list file

optional arguments:
  --format {text,json,csv}
                        Output format (default: json)
  --output OUTPUT       Write output to file
  --parallel            Run checks in parallel (faster for many devices)
```

### monitor

```
$ integrity-checker monitor --help
usage: integrity-checker monitor [-h] --device DEVICE [--interval INTERVAL]
                                  [--alert-on-fail] [--webhook WEBHOOK_URL]

required arguments:
  --device DEVICE       Device IP:PORT

optional arguments:
  --interval INTERVAL   Check interval in seconds (default: 300)
  --alert-on-fail       Print alert when integrity check fails
  --webhook WEBHOOK_URL Send alerts to webhook URL
```

---

## Cloud Phone Integration

`integrity-checker` was designed for cloud phone fleet management:

### Deploy on qtphone.com

```bash
# Connect to your qtphone cloud phone
integrity-checker check --device <qtphone-ip>:5555

# Batch check all phones in your fleet
integrity-checker batch --file qtphone-fleet.txt --parallel --output fleet-report.json
```

### Integration with monitoring systems

Send alerts to your monitoring stack:

```bash
# Slack webhook
integrity-checker monitor --device 192.168.1.100:5555 \
  --interval 300 \
  --webhook https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Discord webhook
integrity-checker monitor --device 192.168.1.100:5555 \
  --interval 300 \
  --webhook https://discord.com/api/webhooks/your/webhook
```

### REST API

Start a server for remote checks:

```bash
integrity-checker serve --port 8080 --host 0.0.0.0

# Then check via HTTP:
curl http://localhost:8080/check/192.168.1.100:5555
```

---

## Architecture

```
integrity-checker/
├── integrity_checker/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point
│   ├── checker.py          # Core integrity check logic
│   ├── adb_client.py       # ADB communication
│   ├── formatter.py        # Output formatters (text/json/csv)
│   ├── monitor.py          # Continuous monitoring
│   └── api_server.py       # REST API server
├── tests/
│   ├── test_checker.py
│   └── test_adb_client.py
├── requirements.txt
├── setup.py
└── README.md
```

---

## How It Works

1. **ADB Connection** — Connects to Android device via ADB
2. **Play Services Query** — Queries Google Play Services for integrity verdict
3. **Result Parsing** — Parses JSON response from Play Integrity API
4. **Report Generation** — Formats and displays/saves the result

The tool uses the official Google Play Integrity API via Play Services running on the device. No Google API key required for basic checks.

---

## Prerequisites

- Python 3.8+
- ADB (Android Debug Bridge) installed and in PATH
- Target device: Android 8.0+ with Google Play Services
- Target device: ADB debugging enabled

### Enable ADB on your cloud phone

```bash
# On your Android device (via terminal or cloud console):
# Settings → About → Tap "Build Number" 7 times
# Settings → Developer Options → Enable USB Debugging / Wireless ADB
```

---

## Troubleshooting

### "Device not found"

```bash
# Verify ADB connection
adb devices -l

# Reconnect
adb connect <device-ip>:5555
```

### "Play Services not installed"

Install Google Play Services on your cloud phone:
- **Easy way**: Use a [qtphone.com](https://www.qtphone.com) image with GMS pre-installed
- **Manual**: Follow our [cloud-phone-gms-guide](https://github.com/luoshixin93-sudo/cloud-phone-gms-guide)

### "Integrity checks failing on rooted device"

Install these Magisk modules:
1. [PlayIntegrityFix](https://github.com/chiteroman/PlayIntegrityFix)
2. [Universal SafetyNet Fix](https://github.com/kdrag0n/safetynet-fix)

Then re-check.

---

## License

**MIT License** — Use freely for personal, commercial, and educational purposes.

---

## Related Projects

| Project | Description |
|---------|-------------|
| [PlayIntegrityFix](https://github.com/chiteroman/PlayIntegrityFix) | Magisk module to fix Play Integrity |
| [Universal SafetyNet Fix](https://github.com/kdrag0n/safetynet-fix) | SafetyNet & Play Integrity bypass |
| [YASNAC](https://github.com/RikkaApps/YASNAC) | Yet Another SafetyNet Attestation Check |
| [cloud-phone-gms-guide](https://github.com/luoshixin93-sudo/cloud-phone-gms-guide) | Install GMS on cloud phones |
| [play-integrity-helper](https://github.com/luoshixin93-sudo/play-integrity-helper) | Automate Play Integrity setup |

---

## Cloud Phone Platform

Need cloud phones that pass Play Integrity checks reliably?

👉 **[qtphone.com](https://www.qtphone.com)** — Cloud Android phones with pre-installed GMS and integrity optimization.

- Fleet management dashboard
- ADB access included
- Integrity-optimized images
- Scale from 1 to 1000+ devices
