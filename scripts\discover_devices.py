#!/usr/bin/env python3
"""
Discover Xiaomi devices
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.tts_bridge import discover_devices, run_async


def main():
    """Discover and list Xiaomi devices"""
    # Load environment variables
    load_dotenv()
    
    # Get credentials
    username = os.getenv("XIAOMI_USERNAME")
    password = os.getenv("XIAOMI_PASSWORD")
    
    if not username or not password:
        print("Error: XIAOMI_USERNAME and XIAOMI_PASSWORD must be set")
        print("\nPlease set them in your .env file:")
        print("XIAOMI_USERNAME=your_username")
        print("XIAOMI_PASSWORD=your_password")
        print("\nOr run with environment variables:")
        print("XIAOMI_USERNAME=xxx XIAOMI_PASSWORD=xxx python discover_devices.py")
        sys.exit(1)
    
    print("Discovering Xiaomi devices...")
    print("=" * 60)
    
    # Discover devices
    result = run_async(discover_devices(username, password))
    
    if not result["success"]:
        print(f"Error: {result['error']}")
        sys.exit(1)
    
    devices = result["devices"]
    
    if not devices:
        print("No devices found.")
        print("\nPossible reasons:")
        print("1. Wrong username/password")
        print("2. No devices linked to account")
        print("3. Network connectivity issues")
        print("4. Xiaomi service maintenance")
        sys.exit(1)
    
    print(f"Found {len(devices)} device(s):")
    print("=" * 60)
    
    for i, device in enumerate(devices, 1):
        status = "✓ Online" if device["online"] else "✗ Offline"
        
        print(f"\n{i}. {device['name']} ({device['model']})")
        print(f"   Status: {status}")
        print(f"   Device ID: {device['device_id']}")
        print(f"   Volume: {device['volume']}")
    
    print("\n" + "=" * 60)
    print("To use a device, copy its Device ID to your .env file:")
    print("XIAOMI_DEVICE_ID=your_device_id_here")
    print("\nRecommended device types for TTS:")
    print("- Xiao Ai Speaker Play (LX05)")
    print("- Xiao Ai Speaker (other models)")
    print("- Mi Smart Speaker")
    print("\nNote: Some devices may not support TTS via this API.")


if __name__ == "__main__":
    main()