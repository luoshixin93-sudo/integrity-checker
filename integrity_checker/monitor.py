"""Continuous monitoring for integrity checks."""
import time
import requests
from .checker import IntegrityChecker

class Monitor:
    """Continuous integrity monitoring."""

    def __init__(self, device, interval, alert_on_fail, webhook):
        self.device = device
        self.interval = interval
        self.alert_on_fail = alert_on_fail
        self.webhook = webhook

    def run(self):
        """Run continuous monitoring loop."""
        print(f"Monitoring {self.device} every {self.interval}s. Press Ctrl+C to stop.")
        last_status = None

        while True:
            try:
                checker = IntegrityChecker(self.device)
                result = checker.run_check()
                status = result.get("overall", "FAIL")

                timestamp = result.get("timestamp", "")
                if status == "PASS":
                    print(f"[{timestamp}] ✅ PASS — {self.device}")
                else:
                    print(f"[{timestamp}] ❌ FAIL — {self.device}")
                    if self.alert_on_fail and status != last_status:
                        self._send_alert(result)

                last_status = status
            except Exception as e:
                print(f"[ERROR] {self.device}: {e}")

            time.sleep(self.interval)

    def _send_alert(self, result):
        """Send alert via webhook."""
        if not self.webhook:
            return
        try:
            message = {
                "text": f"⚠️ Integrity Check FAILED on {self.device}\n"
                        f"Device: {result.get('device')}\n"
                        f"Android: {result.get('android_version')}\n"
                        f"Basic Integrity: {result.get('basic_integrity')}\n"
                        f"CTS Profile: {result.get('cts_profile_match')}"
            }
            requests.post(self.webhook, json=message, timeout=10)
            print(f"Alert sent to webhook")
        except Exception as e:
            print(f"Failed to send alert: {e}")
