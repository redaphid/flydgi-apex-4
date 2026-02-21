#!/bin/bash
# Flydigi Apex 4 Protocol Investigation Toolkit
# Run with: ./start.sh [tool] [args]
# Examples:
#   ./start.sh enumerate
#   ./start.sh probe
#   ./start.sh sniff --duration 120

TOOL="${1:-enumerate}"

case "$TOOL" in
  enumerate|enum)
    uv run enumerate_apex4.py
    ;;
  probe|features)
    uv run probe_features.py
    ;;
  sniff|capture)
    shift
    uv run sniff_vendor_iface.py "$@"
    ;;
  help|--help|-h)
    echo "Usage: ./start.sh [tool] [args]"
    echo ""
    echo "Tools:"
    echo "  enumerate  - Scan for Apex 4 and identify HID interfaces"
    echo "  probe      - Read feature reports from HID interfaces"
    echo "  sniff      - Capture packets from vendor interfaces"
    echo ""
    echo "Examples:"
    echo "  ./start.sh enumerate"
    echo "  ./start.sh sniff --duration 120"
    ;;
  *)
    echo "Unknown tool: $TOOL"
    echo "Run './start.sh help' for usage"
    exit 1
    ;;
esac
