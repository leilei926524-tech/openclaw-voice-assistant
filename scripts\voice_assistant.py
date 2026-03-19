#!/usr/bin/env python3
"""
Voice Assistant Core
Integrates TTS with text processing and filtering
"""

import re
import os
import sys
import threading
import asyncio
from typing import Optional, Dict, Any, Callable
from pathlib import Path

from dotenv import load_dotenv

# Import TTS bridge
from .tts_bridge import TTSBridge, run_async


class VoiceAssistant:
    """Main voice assistant class"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize voice assistant
        
        Args:
            config_path: Path to config file
        """
        if config_path:
            load_dotenv(config_path)
        
        # Configuration
        self.voice_enabled = os.getenv("VOICE_ENABLED", "true").lower() == "true"
        self.min_length = int(os.getenv("VOICE_MIN_LENGTH", "10"))
        self.max_length = int(os.getenv("VOICE_MAX_LENGTH", "300"))
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        
        # TTS bridge
        self.tts_bridge = TTSBridge(config_path)
        
        # State
        self._speaking = False
        self._queue = []
        self._lock = threading.Lock()
        
        # Callbacks
        self.on_speak_start: Optional[Callable[[str], None]] = None
        self.on_speak_end: Optional[Callable[[str, bool], None]] = None
        self.on_error: Optional[Callable[[str, Exception], None]] = None
    
    def enable(self):
        """Enable voice output"""
        self.voice_enabled = True
        if self.debug:
            print("[VOICE] Voice enabled")
    
    def disable(self):
        """Disable voice output"""
        self.voice_enabled = False
        if self.debug:
            print("[VOICE] Voice disabled")
    
    def is_enabled(self) -> bool:
        """Check if voice is enabled"""
        return self.voice_enabled
    
    def clean_text(self, text: str) -> str:
        """
        Clean text for TTS
        
        Args:
            text: Input text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove code blocks
        text = re.sub(r'```[\s\S]*?```', '', text)
        
        # Remove inline code
        text = re.sub(r'`[^`]*`', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Remove markdown links
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # Remove markdown formatting
        text = re.sub(r'[*_~#>]', '', text)
        
        # Remove emojis and special characters
        text = re.sub(r'[^\w\s,.!?;:\-\'"()]', '', text)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def should_speak(self, text: str) -> bool:
        """
        Check if text should be spoken
        
        Args:
            text: Text to check
            
        Returns:
            True if should be spoken
        """
        if not self.voice_enabled:
            return False
        
        clean_text = self.clean_text(text)
        
        # Check length
        if len(clean_text) < self.min_length:
            if self.debug:
                print(f"[VOICE] Skipping: too short ({len(clean_text)} chars)")
            return False
        
        if len(clean_text) > self.max_length:
            if self.debug:
                print(f"[VOICE] Skipping: too long ({len(clean_text)} chars)")
            return False
        
        # Check for code
        if '```' in text or '`' in text:
            if self.debug:
                print("[VOICE] Skipping: contains code")
            return False
        
        # Check for URLs
        if 'http://' in text or 'https://' in text:
            if self.debug:
                print("[VOICE] Skipping: contains URLs")
            return False
        
        # Check if text is mostly non-speakable
        if len(clean_text) < len(text) * 0.3:  # Less than 30% clean text
            if self.debug:
                print("[VOICE] Skipping: mostly non-speakable content")
            return False
        
        return True
    
    def speak(self, text: str, async_mode: bool = True) -> bool:
        """
        Speak text
        
        Args:
            text: Text to speak
            async_mode: Run in background thread
            
        Returns:
            True if speaking started successfully
        """
        if not self.should_speak(text):
            return False
        
        clean_text = self.clean_text(text)
        
        if self.debug:
            print(f"[VOICE] Speaking: {clean_text[:80]}...")
        
        # Call on_speak_start callback
        if self.on_speak_start:
            try:
                self.on_speak_start(clean_text)
            except Exception as e:
                if self.debug:
                    print(f"[VOICE] Callback error: {e}")
        
        # Mark as speaking
        with self._lock:
            self._speaking = True
        
        # Speak in background thread
        if async_mode:
            thread = threading.Thread(
                target=self._speak_thread,
                args=(clean_text,),
                daemon=True
            )
            thread.start()
            return True
        else:
            # Speak synchronously
            success = self._speak_sync(clean_text)
            
            # Mark as not speaking
            with self._lock:
                self._speaking = False
            
            # Call on_speak_end callback
            if self.on_speak_end:
                try:
                    self.on_speak_end(clean_text, success)
                except Exception as e:
                    if self.debug:
                        print(f"[VOICE] Callback error: {e}")
            
            return success
    
    def _speak_thread(self, text: str):
        """Background thread for speaking"""
        try:
            success = self._speak_sync(text)
            
            # Mark as not speaking
            with self._lock:
                self._speaking = False
            
            # Call on_speak_end callback
            if self.on_speak_end:
                try:
                    self.on_speak_end(text, success)
                except Exception as e:
                    if self.debug:
                        print(f"[VOICE] Callback error: {e}")
                        
        except Exception as e:
            # Mark as not speaking
            with self._lock:
                self._speaking = False
            
            # Call error callback
            if self.on_error:
                try:
                    self.on_error(text, e)
                except:
                    pass
            
            if self.debug:
                print(f"[VOICE] Thread error: {e}")
    
    def _speak_sync(self, text: str) -> bool:
        """Synchronous speaking"""
        try:
            result = run_async(self.tts_bridge.speak(text))
            
            if result["success"]:
                if self.debug:
                    print(f"[VOICE] Success: {result.get('message', 'Sent')}")
                return True
            else:
                if self.debug:
                    print(f"[VOICE] Failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            if self.debug:
                print(f"[VOICE] Exception: {e}")
            return False
    
    def is_speaking(self) -> bool:
        """Check if currently speaking"""
        with self._lock:
            return self._speaking
    
    def wait_until_done(self, timeout: Optional[float] = None):
        """
        Wait until speaking is done
        
        Args:
            timeout: Timeout in seconds
        """
        import time
        
        start_time = time.time()
        while self.is_speaking():
            if timeout and time.time() - start_time > timeout:
                break
            time.sleep(0.1)
    
    def test(self) -> Dict[str, Any]:
        """
        Test voice assistant functionality
        
        Returns:
            Test results
        """
        tests = []
        
        # Test 1: TTS bridge connection
        tts_test = run_async(self.tts_bridge.test_connection())
        tests.append({
            "name": "TTS Bridge Connection",
            "success": tts_test["success"],
            "details": tts_test.get("device", {})
        })
        
        # Test 2: Text cleaning
        test_cases = [
            ("Hello **world**!", "Hello world!"),
            ("Visit https://example.com", "Visit"),
            ("Code: `print('hello')`", "Code:"),
            ("Normal text", "Normal text")
        ]
        
        cleaning_results = []
        for input_text, expected in test_cases:
            cleaned = self.clean_text(input_text)
            success = cleaned == expected
            cleaning_results.append({
                "input": input_text,
                "cleaned": cleaned,
                "expected": expected,
                "success": success
            })
        
        cleaning_success = all(r["success"] for r in cleaning_results)
        tests.append({
            "name": "Text Cleaning",
            "success": cleaning_success,
            "details": cleaning_results
        })
        
        # Test 3: Should speak logic
        speak_tests = [
            ("Short", False),  # Too short
            ("This is a longer text that should be spoken", True),
            ("Code `print()` here", False),  # Contains code
            ("http://example.com link", False),  # Contains URL
        ]
        
        speak_results = []
        for text, expected in speak_tests:
            result = self.should_speak(text)
            success = result == expected
            speak_results.append({
                "text": text,
                "should_speak": result,
                "expected": expected,
                "success": success
            })
        
        speak_success = all(r["success"] for r in speak_results)
        tests.append({
            "name": "Should Speak Logic",
            "success": speak_success,
            "details": speak_results
        })
        
        # Overall result
        all_success = all(t["success"] for t in tests)
        
        return {
            "success": all_success,
            "tests": tests,
            "voice_enabled": self.voice_enabled,
            "config": {
                "min_length": self.min_length,
                "max_length": self.max_length,
                "debug": self.debug
            }
        }


def respond_with_voice(
    user_message: str,
    ai_response: str,
    voice_assistant: Optional[VoiceAssistant] = None,
    print_response: bool = True
) -> str:
    """
    Helper function to respond with voice
    
    Args:
        user_message: User's message (for context)
        ai_response: AI's response text
        voice_assistant: VoiceAssistant instance (creates new if None)
        print_response: Print AI response to console
        
    Returns:
        AI response text
    """
    # Create voice assistant if not provided
    if voice_assistant is None:
        voice_assistant = VoiceAssistant()
    
    # Print AI response
    if print_response:
        print(f"\n[AI] {ai_response}")
    
    # Speak if appropriate
    if voice_assistant.should_speak(ai_response):
        clean_text = voice_assistant.clean_text(ai_response)
        print(f"[VOICE] Speaking: {clean_text[:80]}...")
        voice_assistant.speak(ai_response)
    else:
        print("[VOICE] Skipping (content not suitable)")
    
    return ai_response


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Voice Assistant")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--speak", help="Text to speak")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--enable", action="store_true", help="Enable voice")
    parser.add_argument("--disable", action="store_true", help="Disable voice")
    parser.add_argument("--status", action="store_true", help="Show status")
    
    args = parser.parse_args()
    
    assistant = VoiceAssistant(args.config)
    
    if args.test:
        print("Running voice assistant tests...")
        print("=" * 50)
        
        result = assistant.test()
        
        if result["success"]:
            print("✓ All tests passed!")
        else:
            print("✗ Some tests failed")
        
        print("\nTest Details:")
        print("-" * 30)
        
        for test in result["tests"]:
            status = "✓" if test["success"] else "✗"
            print(f"{status} {test['name']}")
            
            if not test["success"] and "details" in test:
                for detail in test["details"]:
                    if not detail.get("success", True):
                        print(f"  - Failed: {detail}")
        
        print(f"\nConfiguration:")
        print(f"  Voice enabled: {result['voice_enabled']}")
        print(f"  Min length: {result['config']['min_length']}")
        print(f"  Max length: {result['config']['max_length']}")
    
    elif args.speak:
        if assistant.speak(args.speak):
            print(f"✓ Speaking: '{args.speak}'")
            assistant.wait_until_done(timeout=10)
        else:
            print(f"✗ Failed to speak: '{args.speak}'")
    
    elif args.enable:
        assistant.enable()
        print("✓ Voice enabled")
    
    elif args.disable:
        assistant.disable()
        print("✓ Voice disabled")
    
    elif args.status:
        test_result = run_async(assistant.tts_bridge.test_connection())
        
        print("Voice Assistant Status:")
        print("=" * 30)
        print(f"Voice enabled: {assistant.is_enabled()}")
        print(f"Currently speaking: {assistant.is_speaking()}")
        
        if test_result["success"]:
            device = test_result["device"]
            print(f"\nDevice: {device['name']} ({device['model']})")
            print(f"Status: {'✓ Online' if device['online'] else '✗ Offline'}")
            print(f"Volume: {device['volume']}")
        else:
            print(f"\n✗ Device connection: {test_result.get('error', 'Unknown error')}")
    
    else:
        parser.print_help()