# Next Steps: Protocol Investigation Setup

After familiarizing yourself with the enumeration and sniffing tools, the next phase is deeper packet analysis and protocol documentation.

## Install Wireshark on Windows

Wireshark is essential for offline packet analysis and will help visualize the USB HID traffic patterns.

### Download & Install

1. Go to https://www.wireshark.org/download/
2. Download the **Windows Installer (64-bit)** — latest stable version
3. Run the installer and accept defaults
4. During installation, when prompted to install **Npcap**, accept it — this enables packet capture on Windows
5. Restart your system

### Verify Installation

```powershell
wireshark --version
```

## Capture USB Traffic with Wireshark

Once installed, you can capture HID traffic directly:

1. Open Wireshark
2. Select your USB interface (usually appears as "usbmon0" or similar on Windows)
3. Start capture
4. Interact with your Apex 4 (upload GIF to screen via Space Station)
5. Stop capture and examine packets
6. Export packets as `.pcapng` for archival

Alternatively, use the JSON exports from `sniff_vendor_iface.py` and manually convert to `.pcap` format if needed.

## Parallel Investigation: Feature Report Analysis

While setting up Wireshark, run feature report probing:

```bash
./start.sh probe
```

This generates `apex4_features_*.json` files. Analyze these to find:
- Which report IDs are readable
- What data structure they contain
- Patterns that might indicate screen control

## Document the Protocol

Create `docs/protocol.md` as you discover patterns:

- Map out report IDs and their purposes
- Document the GIF encoding format (resolution, color depth, frame rate)
- Note any handshake or initialization sequences
- Record timing relationships between packets

## Next Investigation Order

1. ✅ Enumeration (already done)
2. ⏳ Feature report probing → `apex4_features_*.json`
3. ⏳ Packet sniffing + Wireshark analysis → visual protocol mapping
4. ⏳ Documentation in `docs/protocol.md`
5. ⏳ (Optional) Write implementation for screen uploads

## Tools Reference

- **Python scripts** — Quick discovery, JSON export for further analysis
- **Wireshark** — Visual packet inspection, filtering, timeline analysis
- **Text editor** — Document patterns as they emerge

## Windows Quirks to Remember

- USB device drivers on Windows can be strict; if the controller disconnects, replug it
- Wireshark on Windows requires **Npcap** driver for USB capture
- File paths use backslashes (`\`) — the Python scripts handle this, but be aware in manual commands
- Use PowerShell for better command-line experience than cmd.exe

## Resources

- [Wireshark USB Capture Guide](https://wiki.wireshark.org/CaptureSetup/USB)
- [HID Specification](https://www.usb.org/hid)
- [hidapi Documentation](https://github.com/libusb/hidapi)

See [AGENTS.md](AGENTS.md) for protocol investigation progress tracking.
