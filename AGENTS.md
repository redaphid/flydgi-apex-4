# Flydigi Apex 4 Protocol Investigation

## Overview

Reverse-engineering toolkit for the Flydigi Apex 4 gaming controller's HID protocol. Focus is on understanding the screen upload mechanism through vendor-specific HID interfaces.

## Architecture

Three complementary Python tools, each focusing on a different aspect of protocol discovery:

1. **enumerate_apex4.py** — HID device discovery and interface classification
   - Uses the `hidapi` library to scan for Apex 4 (VID:0x04B4, PID:0x2412)
   - Categorizes interfaces by usage page: gamepad (0x0001), mouse (0x0001), vendor (0xFFA0, 0xFFEF)
   - The vendor interfaces are the target for screen protocol work

2. **probe_features.py** — Feature report enumeration
   - Attempts to read feature reports from all interfaces (report IDs 0-255)
   - Saves readable reports to JSON for analysis
   - Non-destructive; only reads existing state

3. **sniff_vendor_iface.py** — Packet capture during operation
   - Non-blocking listener on vendor interfaces
   - Logs packets with timestamps and hex dumps
   - Designed to capture data flow while uploading GIFs via Space Station
   - Can target all vendor interfaces or a specific interface number

## Known Interfaces

From enumeration:
- Interface with usage_page=0x0001, usage=0x0005: Gamepad (controller inputs)
- Interface with usage_page=0x0001, usage=0x0001: Mouse (gyro mode)
- Interface with usage_page=0xFFA0: Vendor (likely screen-related)
- Interface with usage_page=0xFFEF: Vendor (firmware/screen related)

The 0xFFA0 and 0xFFEF interfaces are the primary investigation targets.

## Investigation Progress

- [x] Device enumeration and interface identification
- [x] Feature report probing capability
- [x] Packet capture infrastructure
- [ ] Protocol reverse engineering (in progress)
- [ ] Screen upload protocol documentation
- [ ] Write capability (intentionally deferred)

## Usage Pattern

Typical session:
1. Run `enumerate_apex4.py` to confirm interface layout
2. If probing: `python probe_features.py` to save readable feature reports
3. For live capture: `python sniff_vendor_iface.py --duration 120` while interacting with Space Station

## Dependencies

- Python 3.11+
- hidapi (via `uv sync`)

## Notes for Future Work

The screen protocol likely uses:
- Vendor output reports or feature reports
- May require write commands to trigger responses
- Data flow to watch: GIF encoding → USB packets → screen render

All scripts are read-only by design to ensure safe exploration.
