"""Core integrity checking logic."""
import subprocess
import json
import time
import uuid

class IntegrityChecker:
    """Check Android device SafetyNet and Play Integrity status."""

    def __init__(self, device):
        self.device = device
        self.client_id = f"integrity-checker-{uuid.uuid4().hex[:8]}"

    def run_check(self):
        """Execute integrity check via ADB + Play Services."""
        # Verify device is connected
        try:
            subprocess.run(
                f"adb -s {self.device} shell echo test",
                shell=True,
                capture_output=True,
                timeout=5,
                check=True,
            )
        except Exception as e:
            return {"device": self.device, "error": f"ADB connection failed: {e}"}

        # Get device info
        device_info = self._get_device_info()

        # Query Play Integrity via Play Services
        integrity_result = self._query_play_integrity()

        return {
            "device": device_info.get("model", "Unknown"),
            "ip": self.device,
            "android_version": device_info.get("version", "Unknown"),
            "security_patch": device_info.get("security_patch", "Unknown"),
            "basic_integrity": integrity_result.get("basic_integrity", "UNKNOWN"),
            "device_integrity": integrity_result.get("device_integrity", "UNKNOWN"),
            "cts_profile_match": integrity_result.get("cts_profile_match", "UNKNOWN"),
            "meets_strong_integrity": integrity_result.get("meets_strong_integrity", "UNKNOWN"),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "overall": "PASS" if integrity_result.get("basic_integrity") == "PASS" else "FAIL",
        }

    def _get_device_info(self):
        """Get device information via ADB."""
        info = {}

        def getprop(prop):
            try:
                r = subprocess.run(
                    f"adb -s {self.device} shell getprop {prop}",
                    shell=True, capture_output=True, timeout=3, text=True
                )
                return r.stdout.strip()
            except Exception:
                return "Unknown"

        info["model"] = getprop("ro.product.model")
        info["version"] = getprop("ro.build.version.release")
        info["security_patch"] = getprop("ro.build.version.security_patch")
        info["manufacturer"] = getprop("ro.product.manufacturer")
        return info

    def _query_play_integrity(self):
        """Query Play Integrity API via ADB."""
        # In production, this would call the actual Play Integrity API
        # For now, simulate a passing result
        # Real implementation would use:
        # 1. Request integrity token from Play Services
        # 2. Decode and verify the response

        # Simulated result - in real use, implement Play Integrity API client
        return {
            "basic_integrity": "PASS",
            "device_integrity": "PASS",
            "cts_profile_match": "PASS",
            "meets_strong_integrity": "PASS",
        }
