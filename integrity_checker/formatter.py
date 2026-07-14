"""Output formatters for integrity checker."""
import json
from rich.table import Table
from rich.console import Console

class Formatter:
    """Format integrity check results."""

    @staticmethod
    def format(result, fmt="text"):
        if fmt == "json":
            return json.dumps(result, indent=2, ensure_ascii=False)
        elif fmt == "csv":
            return Formatter._to_csv([result])
        else:
            return Formatter._to_text(result)

    @staticmethod
    def format_batch(results, fmt="json"):
        if fmt == "json":
            return json.dumps(results, indent=2, ensure_ascii=False)
        elif fmt == "csv":
            return Formatter._to_csv(results)
        else:
            lines = []
            for r in results:
                lines.append(Formatter._to_text(r))
                lines.append("")
            return "\n".join(lines)

    @staticmethod
    def _to_text(result):
        console = Console()
        output = []
        overall = result.get("overall", "FAIL")

        # Header
        output.append("╔══════════════════════════════════════════════════════╗")
        output.append("║         Android Device Integrity Report              ║")
        output.append("╠══════════════════════════════════════════════════════╣")
        output.append(f"║  Device:        {result.get('device', 'N/A'):<30}║")
        output.append(f"║  Android:       {result.get('android_version', 'N/A'):<30}║")
        output.append(f"║  Security Patch: {result.get('security_patch', 'N/A'):<29}║")
        output.append("╠══════════════════════════════════════════════════════╣")

        checks = [
            ("Basic Integrity", result.get("basic_integrity")),
            ("Device Integrity", result.get("device_integrity")),
            ("CTS Profile Match", result.get("cts_profile_match")),
            ("Strong Integrity", result.get("meets_strong_integrity")),
        ]

        for name, status in checks:
            icon = "✅ PASS" if status == "PASS" else "❌ FAIL"
            output.append(f"║  {name:<20} {icon:<29}║")

        output.append("╠══════════════════════════════════════════════════════╣")
        overall_icon = "✅ ALL CHECKS PASSED" if overall == "PASS" else "❌ SOME CHECKS FAILED"
        output.append(f"║  Overall:        {overall_icon:<29}║")
        output.append(f"║  Timestamp:      {result.get('timestamp', 'N/A'):<29}║")
        output.append("╚══════════════════════════════════════════════════════╝")

        return "\n".join(output)

    @staticmethod
    def _to_csv(results):
        if not results:
            return ""
        keys = ["device", "ip", "android_version", "security_patch",
                "basic_integrity", "device_integrity", "cts_profile_match",
                "meets_strong_integrity", "overall", "timestamp"]
        header = ",".join(keys)
        rows = []
        for r in results:
            row = [str(r.get(k, "")) for k in keys]
            rows.append(",".join(f'"{v}"' if "," in v else v for v in row))
        return header + "\n" + "\n".join(rows)
