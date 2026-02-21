"""
Sniff the vendor-specific HID interfaces on the Flydigi Apex 4.

This listens on the vendor interfaces (0xffa0 and 0xffef) and logs any
data that comes through. Run this WHILE using Space Station to upload
a GIF to the screen — we want to capture those packets.

Usage:
    python sniff_vendor_iface.py [--duration SECONDS] [--interface INDEX]
"""
import hid
import time
import sys
import argparse
import json
from datetime import datetime

FLYDIGI_VID = 0x04B4
FLYDIGI_PID = 0x2412

VENDOR_USAGE_PAGES = [0xFFA0, 0xFFEF]


def find_vendor_interfaces():
    """Find all vendor-specific HID interfaces on the Apex 4."""
    devices = hid.enumerate(FLYDIGI_VID, FLYDIGI_PID)
    vendor_devs = [d for d in devices if d["usage_page"] in VENDOR_USAGE_PAGES]
    return vendor_devs


def sniff_interface(dev_info, duration, output_file):
    """Open a HID interface and log all incoming data."""
    up = dev_info["usage_page"]
    iface = dev_info["interface_number"]
    print(f"Opening interface {iface} (usage_page=0x{up:04x})...")

    device = hid.device()
    device.open_path(dev_info["path"])
    device.set_nonblocking(True)

    print(f"Listening for {duration}s... (interact with Space Station now!)")
    print("-" * 70)

    packets = []
    start = time.time()
    packet_count = 0

    try:
        while time.time() - start < duration:
            data = device.read(256)
            if data:
                elapsed = time.time() - start
                hex_data = data.hex() if isinstance(data, bytes) else bytes(data).hex()
                packet_count += 1

                entry = {
                    "time": round(elapsed, 4),
                    "iface": iface,
                    "usage_page": f"0x{up:04x}",
                    "len": len(data),
                    "hex": hex_data,
                }
                packets.append(entry)

                # Print live
                preview = hex_data[:80]
                if len(hex_data) > 80:
                    preview += "..."
                print(f"  [{elapsed:8.4f}s] iface={iface} len={len(data):3d} | {preview}")
            else:
                time.sleep(0.001)  # 1ms poll
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        device.close()

    print("-" * 70)
    print(f"Captured {packet_count} packets from interface {iface}")

    if output_file and packets:
        with open(output_file, "w") as f:
            json.dump(packets, f, indent=2)
        print(f"Saved to {output_file}")

    return packets


def sniff_all_vendor_interfaces(duration, output_prefix):
    """Sniff all vendor interfaces simultaneously using non-blocking reads."""
    vendor_devs = find_vendor_interfaces()
    if not vendor_devs:
        print("No vendor interfaces found! Is the controller in DInput mode?")
        return

    print(f"Found {len(vendor_devs)} vendor interface(s):")
    for d in vendor_devs:
        print(f"  iface={d['interface_number']} usage_page=0x{d['usage_page']:04x}")

    # Open all devices
    handles = []
    for dev_info in vendor_devs:
        try:
            device = hid.device()
            device.open_path(dev_info["path"])
            device.set_nonblocking(True)
            handles.append((device, dev_info))
            print(f"  Opened interface {dev_info['interface_number']}")
        except Exception as e:
            print(f"  FAILED to open interface {dev_info['interface_number']}: {e}")

    if not handles:
        print("Could not open any interfaces!")
        return

    print(f"\nListening for {duration}s... Open Space Station and upload a GIF now!")
    print("=" * 70)

    all_packets = []
    start = time.time()

    try:
        while time.time() - start < duration:
            got_data = False
            for device, dev_info in handles:
                data = device.read(256)
                if data:
                    got_data = True
                    elapsed = time.time() - start
                    iface = dev_info["interface_number"]
                    up = dev_info["usage_page"]
                    hex_data = data.hex() if isinstance(data, bytes) else bytes(data).hex()

                    entry = {
                        "time": round(elapsed, 4),
                        "iface": iface,
                        "usage_page": f"0x{up:04x}",
                        "len": len(data),
                        "hex": hex_data,
                    }
                    all_packets.append(entry)

                    preview = hex_data[:80]
                    if len(hex_data) > 80:
                        preview += "..."
                    print(f"  [{elapsed:8.4f}s] iface={iface} up=0x{up:04x} len={len(data):3d} | {preview}")

            if not got_data:
                time.sleep(0.001)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        for device, _ in handles:
            device.close()

    print("=" * 70)
    print(f"Total captured: {len(all_packets)} packets")

    # Save
    if all_packets:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        outfile = f"{output_prefix}_{ts}.json"
        with open(outfile, "w") as f:
            json.dump(all_packets, f, indent=2)
        print(f"Saved to {outfile}")

        # Summary by interface
        by_iface = {}
        for p in all_packets:
            key = p["iface"]
            by_iface.setdefault(key, []).append(p)
        print("\nPackets per interface:")
        for iface, pkts in sorted(by_iface.items()):
            print(f"  Interface {iface}: {len(pkts)} packets")
            # Show unique packet prefixes (first 6 bytes) to identify message types
            prefixes = set()
            for p in pkts:
                prefixes.add(p["hex"][:12])  # first 6 bytes
            if len(prefixes) <= 20:
                print(f"    Unique prefixes (first 6 bytes): {sorted(prefixes)}")
    else:
        print("No packets captured. The vendor interfaces may need write commands to trigger responses.")
        print("Try running the feature report probe script next.")

    return all_packets


def main():
    parser = argparse.ArgumentParser(description="Sniff Flydigi Apex 4 vendor HID interfaces")
    parser.add_argument("--duration", "-d", type=int, default=60,
                        help="Capture duration in seconds (default: 60)")
    parser.add_argument("--output", "-o", default="apex4_capture",
                        help="Output file prefix (default: apex4_capture)")
    parser.add_argument("--interface", "-i", type=int, default=None,
                        help="Specific interface number to sniff (default: all vendor)")
    args = parser.parse_args()

    if args.interface is not None:
        vendor_devs = find_vendor_interfaces()
        target = [d for d in vendor_devs if d["interface_number"] == args.interface]
        if not target:
            print(f"Interface {args.interface} not found among vendor interfaces!")
            return
        sniff_interface(target[0], args.duration,
                        f"{args.output}_iface{args.interface}.json")
    else:
        sniff_all_vendor_interfaces(args.duration, args.output)


if __name__ == "__main__":
    main()
