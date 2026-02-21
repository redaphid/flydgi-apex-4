"""
Probe the Flydigi Apex 4's vendor HID interfaces by sending
feature report requests.

HID devices communicate via:
  - Input reports  (device -> host, polled or interrupt)
  - Output reports (host -> device)
  - Feature reports (bidirectional, get/set configuration)

The screen upload protocol likely uses output reports or feature reports.
This script probes for readable feature reports to map out the protocol.

WARNING: This only READS. It does not write anything to the device.
"""
import hid
import sys
import json
from datetime import datetime

FLYDIGI_VID = 0x04B4
FLYDIGI_PID = 0x2412
VENDOR_USAGE_PAGES = [0xFFA0, 0xFFEF]


def probe_feature_reports(dev_info, report_ids=None):
    """Try to read feature reports from a device."""
    iface = dev_info["interface_number"]
    up = dev_info["usage_page"]

    print(f"\nProbing interface {iface} (usage_page=0x{up:04x})...")
    print("-" * 50)

    device = hid.device()
    try:
        device.open_path(dev_info["path"])
    except Exception as e:
        print(f"  Failed to open: {e}")
        return {}

    if report_ids is None:
        report_ids = range(256)

    results = {}
    for rid in report_ids:
        try:
            data = device.get_feature_report(rid, 256)
            if data:
                hex_data = data.hex() if isinstance(data, bytes) else bytes(data).hex()
                results[rid] = hex_data
                print(f"  Report ID 0x{rid:02x} ({rid:3d}): len={len(data):3d} | {hex_data[:80]}")
        except Exception:
            pass  # Most report IDs won't exist

    device.close()

    if not results:
        print("  No readable feature reports found.")
    else:
        print(f"\n  Found {len(results)} readable feature report(s)")

    return results


def main():
    print("=" * 60)
    print("Flydigi Apex 4 — Feature Report Probe (READ ONLY)")
    print("=" * 60)

    devices = hid.enumerate(FLYDIGI_VID, FLYDIGI_PID)
    if not devices:
        print("No Flydigi Apex 4 found! Is it plugged in and in DInput mode?")
        return

    vendor_devs = [d for d in devices if d["usage_page"] in VENDOR_USAGE_PAGES]
    all_devs = devices  # probe all interfaces, not just vendor

    print(f"Found {len(devices)} interface(s), {len(vendor_devs)} vendor-specific")

    all_results = {}
    for dev_info in all_devs:
        iface = dev_info["interface_number"]
        res = probe_feature_reports(dev_info)
        if res:
            all_results[f"iface_{iface}_0x{dev_info['usage_page']:04x}"] = res

    if all_results:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        outfile = f"apex4_features_{ts}.json"
        with open(outfile, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"\nSaved all results to {outfile}")


if __name__ == "__main__":
    main()
