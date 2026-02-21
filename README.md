# Flydigi Apex 4 Protocol Investigation

Tools for reverse-engineering the HID protocol of the Flydigi Apex 4 gaming controller, particularly the vendor-specific interfaces responsible for screen uploads.

## What This Is

The Flydigi Apex 4 is a gaming controller with an embedded display. This toolkit provides utilities to understand how data flows to the screen through its HID interfaces.

## Tools

**enumerate_apex4.py**
> Scan for connected Apex 4 controllers and identify their HID interfaces. Shows which interface handles the screen protocol.

**probe_features.py**
> Read feature reports from HID interfaces to map readable configuration values. Helps identify protocol structure.

**sniff_vendor_iface.py**
> Capture packets from vendor-specific HID interfaces. Run while uploading a GIF via Space Station to see the actual screen protocol in action.

## Setup

```bash
uv sync
```

## Running

Each script runs independently:

```bash
uv run enumerate_apex4.py
uv run probe_features.py
uv run sniff_vendor_iface.py --duration 60
```

The enumeration tool should be run first to understand your controller's interface layout.

## Notes

- Requires the Flydigi Apex 4 connected via USB
- DInput mode is preferred for broader interface access
- All tools are read-only; no writes to the device

## References

- [AGENTS.md](AGENTS.md) — Detailed protocol notes and investigation progress
- [NEXT_STEPS.md](NEXT_STEPS.md) — Setup for deeper analysis (Wireshark, protocol documentation)
