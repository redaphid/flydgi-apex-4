"""
Enumerate HID devices and find the Flydigi Apex 4 interfaces.
Run this with the controller plugged in (DInput mode recommended).
"""
import hid

# Known Flydigi Apex 4 IDs
FLYDIGI_DINPUT_VID = 0x04B4
FLYDIGI_DINPUT_PID = 0x2412

# XInput mode presents as Xbox 360 controller
XBOX360_VID = 0x045E
XBOX360_PID = 0x028E

print("=" * 70)
print("Scanning for Flydigi Apex 4 HID interfaces...")
print("=" * 70)

all_devices = hid.enumerate()
flydigi_devices = []

for dev in all_devices:
    if (dev["vendor_id"] == FLYDIGI_DINPUT_VID and dev["product_id"] == FLYDIGI_DINPUT_PID):
        flydigi_devices.append(dev)
    elif (dev["vendor_id"] == XBOX360_VID and dev["product_id"] == XBOX360_PID
          and dev["product_string"] and "Flydigi" in dev["product_string"]):
        flydigi_devices.append(dev)

if not flydigi_devices:
    print("\nNo Flydigi Apex 4 found!")
    print("Make sure the controller is:")
    print("  - Plugged in via USB")
    print("  - In DInput mode (preferred) or XInput mode")
    print("\nAll HID devices found:")
    for dev in all_devices:
        if dev["product_string"]:
            print(f"  VID={dev['vendor_id']:04x} PID={dev['product_id']:04x} "
                  f"usage_page=0x{dev['usage_page']:04x} usage=0x{dev['usage']:04x} "
                  f"- {dev['manufacturer_string']} {dev['product_string']}")
else:
    print(f"\nFound {len(flydigi_devices)} Flydigi interface(s):\n")
    for i, dev in enumerate(flydigi_devices):
        print(f"Interface {i}:")
        print(f"  Path:         {dev['path']}")
        print(f"  VID:PID:      {dev['vendor_id']:04x}:{dev['product_id']:04x}")
        print(f"  Manufacturer: {dev['manufacturer_string']}")
        print(f"  Product:      {dev['product_string']}")
        print(f"  Usage Page:   0x{dev['usage_page']:04x}")
        print(f"  Usage:        0x{dev['usage']:04x}")
        print(f"  Interface #:  {dev['interface_number']}")
        print()

    # Identify the interfaces based on known usage pages
    print("-" * 70)
    print("Interface analysis:")
    for dev in flydigi_devices:
        up = dev["usage_page"]
        label = "UNKNOWN"
        if up == 0x0001 and dev["usage"] == 0x0005:
            label = "GAMEPAD (controller inputs)"
        elif up == 0x0001 and dev["usage"] == 0x0001:
            label = "MOUSE (gyro mouse mode)"
        elif up == 0xFFA0:
            label = "VENDOR (Space Station / config) << TARGET FOR SCREEN"
        elif up == 0xFFEF:
            label = "VENDOR (firmware / screen?)     << TARGET FOR SCREEN"
        print(f"  usage_page=0x{up:04x} iface={dev['interface_number']:2d} -> {label}")
