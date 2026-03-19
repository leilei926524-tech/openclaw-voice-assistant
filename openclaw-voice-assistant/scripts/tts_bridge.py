#!/usr/bin/env python3
"""
TTS Bridge for Xiaomi Smart Speakers
Handles authentication and text-to-speech conversion
"""

import asyncio
import os
import sys
from typing import Optional, Dict, Any
from pathlib import Path

import aiohttp
from miservice import MiAccount, MiNAService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TTSBridge:
    """Bridge for Xiaomi TTS service"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize TTS bridge
        
        Args:
            config_path: Path to .env file (default: .env in current directory)
        """
        if config_path:
            load_dotenv(config_path)
        
        self.username = os.getenv("XIAOMI_USERNAME")
        self.password = os.getenv("XIAOMI_PASSWORD")
        self.device_id = os.getenv("XIAOMI_DEVICE_ID")
        self.sid = os.getenv("XIAOMI_SID", "micoapi")
        
        self.session: Optional[aiohttp.ClientSession] = None
        self.account: Optional[MiAccount] = None
        self.mina_service: Optional[MiNAService] = None
        
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration"""
        missing = []
        if not self.username:
            missing.append("XIAOMI_USERNAME")
        if not self.password:
            missing.append("XIAOMI_PASSWORD")
        if not self.device_id:
            missing.append("XIAOMI_DEVICE_ID")
        
        if missing:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing)}. "
                f"Please set them in .env file or environment variables."
            )
    
    async def connect(self):
        """Connect to Xiaomi service"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        
        if self.account is None:
            self.account = MiAccount(
                session=self.session,
                username=self.username,
                password=self.password
            )
            await self.account.login(sid=self.sid)
        
        if self.mina_service is None:
            self.mina_service = MiNAService(self.account)
    
    async def disconnect(self):
        """Disconnect from Xiaomi service"""
        if self.session:
            await self.session.close()
            self.session = None
            self.account = None
            self.mina_service = None
    
    async def speak(self, text: str) -> Dict[str, Any]:
        """
        Send text to speaker for TTS
        
        Args:
            text: Text to speak
            
        Returns:
            Dict with response data
        """
        if not text or not text.strip():
            return {"success": False, "error": "Empty text"}
        
        try:
            await self.connect()
            
            # Send TTS command
            result = await self.mina_service.text_to_speech(self.device_id, text)
            
            # Parse response
            if isinstance(result, dict) and result.get("code") == 0:
                return {
                    "success": True,
                    "code": 0,
                    "message": result.get("message", "TTS command sent"),
                    "data": result.get("data", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"TTS failed: {result}",
                    "raw_response": result
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"TTS error: {str(e)}"
            }
    
    async def get_device_info(self) -> Dict[str, Any]:
        """
        Get information about the connected device
        
        Returns:
            Dict with device information
        """
        try:
            await self.connect()
            
            # Get device info
            devices = await self.mina_service.device_list()
            
            # Find our device
            for device in devices:
                if device.get("deviceID") == self.device_id:
                    return {
                        "success": True,
                        "device": {
                            "name": device.get("name"),
                            "model": device.get("hardware"),
                            "status": device.get("status"),
                            "volume": device.get("volume"),
                            "online": device.get("isOnline", False)
                        }
                    }
            
            return {
                "success": False,
                "error": f"Device {self.device_id} not found"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Device info error: {str(e)}"
            }
    
    async def test_connection(self) -> Dict[str, Any]:
        """
        Test connection and TTS functionality
        
        Returns:
            Dict with test results
        """
        # Test 1: Device info
        device_info = await self.get_device_info()
        if not device_info["success"]:
            return device_info
        
        # Test 2: Simple TTS
        test_text = "Connection test successful."
        tts_result = await self.speak(test_text)
        
        return {
            "success": tts_result["success"],
            "device": device_info.get("device"),
            "tts_test": tts_result,
            "message": "Connection test completed"
        }


async def discover_devices(username: str, password: str) -> Dict[str, Any]:
    """
    Discover available Xiaomi devices
    
    Args:
        username: Xiaomi username
        password: Xiaomi password
        
    Returns:
        Dict with discovered devices
    """
    try:
        session = aiohttp.ClientSession()
        account = MiAccount(session=session, username=username, password=password)
        await account.login(sid="micoapi")
        
        mina_service = MiNAService(account)
        devices = await mina_service.device_list()
        
        await session.close()
        
        # Format device list
        formatted_devices = []
        for device in devices:
            formatted_devices.append({
                "device_id": device.get("deviceID"),
                "name": device.get("name"),
                "model": device.get("hardware"),
                "status": device.get("status"),
                "online": device.get("isOnline", False),
                "volume": device.get("volume", 0)
            })
        
        return {
            "success": True,
            "devices": formatted_devices,
            "count": len(formatted_devices)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Discovery failed: {str(e)}"
        }


def run_async(coro):
    """Run async function in sync context"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="TTS Bridge for Xiaomi Speakers")
    parser.add_argument("--discover", action="store_true", help="Discover devices")
    parser.add_argument("--test", action="store_true", help="Test connection")
    parser.add_argument("--speak", help="Text to speak")
    parser.add_argument("--config", help="Path to config file")
    
    args = parser.parse_args()
    
    if args.discover:
        # Load credentials from env
        load_dotenv(args.config)
        username = os.getenv("XIAOMI_USERNAME")
        password = os.getenv("XIAOMI_PASSWORD")
        
        if not username or not password:
            print("Error: XIAOMI_USERNAME and XIAOMI_PASSWORD must be set")
            sys.exit(1)
        
        result = run_async(discover_devices(username, password))
        if result["success"]:
            print(f"Found {result['count']} device(s):")
            for device in result["devices"]:
                status = "✓ Online" if device["online"] else "✗ Offline"
                print(f"  - {device['name']} ({device['model']})")
                print(f"    ID: {device['device_id']}")
                print(f"    Status: {status}")
                print(f"    Volume: {device['volume']}")
                print()
        else:
            print(f"Error: {result['error']}")
    
    elif args.test:
        bridge = TTSBridge(args.config)
        result = run_async(bridge.test_connection())
        
        if result["success"]:
            print("✓ Connection test successful!")
            device = result["device"]
            print(f"  Device: {device['name']} ({device['model']})")
            print(f"  Status: {'Online' if device['online'] else 'Offline'}")
            print(f"  Volume: {device['volume']}")
        else:
            print(f"✗ Test failed: {result.get('error', 'Unknown error')}")
    
    elif args.speak:
        bridge = TTSBridge(args.config)
        result = run_async(bridge.speak(args.speak))
        
        if result["success"]:
            print(f"✓ Sent: '{args.speak}'")
            print(f"  Response: {result['message']}")
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
    
    else:
        parser.print_help()