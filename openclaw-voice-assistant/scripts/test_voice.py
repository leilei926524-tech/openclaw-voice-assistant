#!/usr/bin/env python3
"""
Test voice functionality
"""

import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.voice_assistant import VoiceAssistant


def main():
    """Test voice assistant"""
    # Load environment variables
    load_dotenv()
    
    print("Voice Assistant Test")
    print("=" * 60)
    
    # Initialize voice assistant
    assistant = VoiceAssistant()
    
    # Run comprehensive test
    test_result = assistant.test()
    
    print("\nTest Results:")
    print("=" * 60)
    
    if test_result["success"]:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
    
    # Show detailed results
    for test in test_result["tests"]:
        status = "✓" if test["success"] else "✗"
        print(f"\n{status} {test['name']}")
        
        if not test["success"]:
            if "details" in test:
                for detail in test["details"]:
                    if not detail.get("success", True):
                        print(f"  - Failed: {detail}")
    
    print(f"\nConfiguration:")
    print(f"  Voice enabled: {test_result['voice_enabled']}")
    print(f"  Min length: {test_result['config']['min_length']}")
    print(f"  Max length: {test_result['config']['max_length']}")
    
    # Interactive test if all passed
    if test_result["success"] and test_result["voice_enabled"]:
        print("\n" + "=" * 60)
        print("Interactive Voice Test")
        print("=" * 60)
        print("Type text to test TTS (or 'exit' to quit):")
        
        while True:
            try:
                text = input("\nTest text: ").strip()
                
                if not text:
                    continue
                
                if text.lower() in ['exit', 'quit', 'q']:
                    break
                
                print(f"Sending: '{text}'")
                
                if assistant.speak(text):
                    print("✓ Command sent")
                    # Wait for speaking to complete
                    assistant.wait_until_done(timeout=10)
                else:
                    print("✗ Failed to send")
                    
            except KeyboardInterrupt:
                print("\n\nTest interrupted.")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed.")
    
    if not test_result["success"]:
        print("\nTroubleshooting tips:")
        print("1. Check .env file configuration")
        print("2. Verify Xiaomi account credentials")
        print("3. Ensure device is online")
        print("4. Check network connectivity")
        print("5. Run discover_devices.py to verify device ID")
        sys.exit(1)


if __name__ == "__main__":
    main()