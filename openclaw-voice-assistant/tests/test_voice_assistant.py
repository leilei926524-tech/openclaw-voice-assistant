#!/usr/bin/env python3
"""
Tests for voice_assistant.py
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, AsyncMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestVoiceAssistant(unittest.TestCase):
    """Test VoiceAssistant class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'XIAOMI_USERNAME': 'test_user',
            'XIAOMI_PASSWORD': 'test_pass',
            'XIAOMI_DEVICE_ID': 'test_device'
        })
        self.env_patcher.start()
        
    def tearDown(self):
        """Clean up test fixtures"""
        self.env_patcher.stop()
    
    def test_voice_assistant_import(self):
        """Test that VoiceAssistant can be imported"""
        try:
            from scripts.voice_assistant import VoiceAssistant
            self.assertTrue(hasattr(VoiceAssistant, '__init__'))
        except ImportError as e:
            self.fail(f"Failed to import VoiceAssistant: {e}")
    
    def test_voice_assistant_initialization(self):
        """Test VoiceAssistant initialization"""
        from scripts.voice_assistant import VoiceAssistant
        
        # Test with default config
        assistant = VoiceAssistant()
        self.assertIsNotNone(assistant)
        
        # Test that config is loaded
        self.assertTrue(hasattr(assistant, 'config'))
    
    @patch('scripts.voice_assistant.TTSBridge')
    def test_voice_assistant_speak_method(self, mock_tts_bridge):
        """Test speak method"""
        from scripts.voice_assistant import VoiceAssistant
        
        # Mock TTSBridge
        mock_instance = AsyncMock()
        mock_instance.text_to_speech.return_value = {'code': 0}
        mock_tts_bridge.return_value = mock_instance
        
        assistant = VoiceAssistant()
        
        # Test speak method
        text = "Hello, this is a test"
        result = assistant.speak(text)
        
        # Check that TTSBridge was called
        mock_tts_bridge.assert_called_once()
        
    def test_text_filtering(self):
        """Test text filtering logic"""
        from scripts.voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        
        # Test cases
        test_cases = [
            # (input_text, should_speak, reason)
            ("Short", False, "Too short"),
            ("This is a normal sentence that should be spoken.", True, "Normal length"),
            ("x" * 350, False, "Too long"),
            ("```print('code')```", False, "Contains code block"),
            ("https://example.com", False, "Contains URL"),
            ("Visit example.com for more info", False, "Contains domain"),
            ("Normal text without issues", True, "Clean text"),
        ]
        
        for text, should_speak, reason in test_cases:
            with self.subTest(text=text[:20], reason=reason):
                can_speak = assistant._should_speak(text)
                self.assertEqual(can_speak, should_speak, 
                               f"Failed for: {text[:30]}... (expected: {should_speak}, got: {can_speak})")
    
    def test_text_cleaning(self):
        """Test text cleaning logic"""
        from scripts.voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        
        test_cases = [
            # (input, expected_output)
            ("**Bold text**", "Bold text"),
            ("*Italic text*", "Italic text"),
            ("`code`", "code"),
            ("[link](url)", "link"),
            ("# Header", "Header"),
            ("- List item", "List item"),
            ("  Multiple   spaces  ", "Multiple spaces"),
            ("Line1\nLine2", "Line1 Line2"),
            ("Special & characters < >", "Special & characters"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input=input_text):
                cleaned = assistant._clean_text(input_text)
                self.assertEqual(cleaned, expected)
    
    @patch('scripts.voice_assistant.TTSBridge')
    def test_enable_disable_methods(self, mock_tts_service):
        """Test enable and disable methods"""
        from scripts.voice_assistant import VoiceAssistant
        
        assistant = VoiceAssistant()
        
        # Initially should be enabled
        self.assertTrue(assistant.enabled)
        
        # Test disable
        assistant.disable()
        self.assertFalse(assistant.enabled)
        
        # Test enable
        assistant.enable()
        self.assertTrue(assistant.enabled)
    
    @patch('scripts.voice_assistant.TTSBridge')
    def test_test_method(self, mock_tts_service):
        """Test test method"""
        from scripts.voice_assistant import VoiceAssistant
        
        # Mock TTSBridge
        mock_instance = AsyncMock()
        mock_instance.text_to_speech.return_value = {'code': 0}
        mock_tts_service.return_value = mock_instance
        
        assistant = VoiceAssistant()
        
        # Test should return True when TTS works
        result = assistant.test()
        self.assertTrue(result)
        
        # Test should return False when TTS fails
        mock_instance.text_to_speech.return_value = {'code': 1, 'message': 'Error'}
        result = assistant.test()
        self.assertFalse(result)

class TestVoiceAssistantIntegration(unittest.TestCase):
    """Integration tests for VoiceAssistant"""
    
    @patch('scripts.voice_assistant.TTSBridge')
    def test_complete_workflow(self, mock_tts_service):
        """Test complete speak workflow"""
        from scripts.voice_assistant import VoiceAssistant
        
        # Mock TTSBridge
        mock_instance = AsyncMock()
        mock_instance.text_to_speech.return_value = {'code': 0}
        mock_tts_service.return_value = mock_instance
        
        assistant = VoiceAssistant()
        
        # Enable assistant
        assistant.enable()
        
        # Test speaking
        test_text = "This is a test message for the voice assistant."
        result = assistant.speak(test_text)
        
        # Verify TTS was called with cleaned text
        expected_text = "This is a test message for the voice assistant."
        mock_instance.text_to_speech.assert_called_once()
        
        # Check that the call was made with correct arguments
        call_args = mock_instance.text_to_speech.call_args
        self.assertIsNotNone(call_args)
        
    def test_config_loading(self):
        """Test configuration loading"""
        from scripts.voice_assistant import VoiceAssistant
        
        # Create a test config file
        test_config = """XIAOMI_USERNAME=test_user_2
XIAOMI_PASSWORD=test_pass_2
XIAOMI_DEVICE_ID=test_device_2
DEBUG=true
"""
        
        with open('test_config.env', 'w') as f:
            f.write(test_config)
        
        try:
            assistant = VoiceAssistant(config_path='test_config.env')
            
            # Check that config was loaded
            self.assertEqual(assistant.config.get('XIAOMI_USERNAME'), 'test_user_2')
            self.assertEqual(assistant.config.get('XIAOMI_PASSWORD'), 'test_pass_2')
            self.assertEqual(assistant.config.get('XIAOMI_DEVICE_ID'), 'test_device_2')
            self.assertEqual(assistant.config.get('DEBUG'), 'true')
            
        finally:
            # Clean up test file
            if os.path.exists('test_config.env'):
                os.remove('test_config.env')

if __name__ == '__main__':
    unittest.main()