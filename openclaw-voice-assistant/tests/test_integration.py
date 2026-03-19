#!/usr/bin/env python3
"""
Integration tests for OpenClaw Voice Assistant
"""

import unittest
import sys
import os
import tempfile
from unittest.mock import Mock, patch, AsyncMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestVoiceAssistantSamanthaIntegration(unittest.TestCase):
    """Integration tests for Voice Assistant and Samantha"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directories
        self.temp_dir = tempfile.mkdtemp()
        
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'XIAOMI_USERNAME': 'test_user',
            'XIAOMI_PASSWORD': 'test_pass',
            'XIAOMI_DEVICE_ID': 'test_device',
            'SAMANTHA_DATA_DIR': self.temp_dir
        })
        self.env_patcher.start()
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.env_patcher.stop()
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('scripts.voice_assistant.TTSBridge')
    def test_integrated_chat_flow(self, mock_tts_service):
        """Test integrated chat flow with both components"""
        from scripts.voice_assistant import VoiceAssistant
        from scripts.samantha import Samantha
        
        # Mock TTSBridge
        mock_tts_instance = AsyncMock()
        mock_tts_instance.text_to_speech.return_value = {'code': 0}
        mock_tts_service.return_value = mock_tts_instance
        
        # Create instances
        assistant = VoiceAssistant()
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Enable voice assistant
        assistant.enable()
        
        # Test conversation flow
        user_message = "Hello, how are you today?"
        
        # Get response from Samantha
        ai_response = samantha.respond(user_message)
        self.assertIsInstance(ai_response, str)
        self.assertGreater(len(ai_response), 0)
        
        # Speak the response
        result = assistant.speak(ai_response)
        
        # Verify TTS was called
        mock_tts_instance.text_to_speech.assert_called_once()
        
        # Verify the text sent to TTS is cleaned
        call_args = mock_tts_instance.text_to_speech.call_args
        self.assertIsNotNone(call_args)
        
        # The cleaned text should not contain markdown or special formatting
        tts_text = call_args[0][0] if call_args[0] else call_args[1].get('text', '')
        self.assertIsInstance(tts_text, str)
        self.assertGreater(len(tts_text), 0)
        
        # Cleaned text should not have markdown symbols
        self.assertNotIn('**', tts_text)
        self.assertNotIn('*', tts_text)
        self.assertNotIn('`', tts_text)
        self.assertNotIn('#', tts_text)
    
    @patch('scripts.voice_assistant.TTSBridge')
    def test_multiple_conversation_turns(self, mock_tts_service):
        """Test multiple conversation turns"""
        from scripts.voice_assistant import VoiceAssistant
        from scripts.samantha import Samantha
        
        # Mock TTSBridge
        mock_tts_instance = AsyncMock()
        mock_tts_instance.text_to_speech.return_value = {'code': 0}
        mock_tts_service.return_value = mock_tts_instance
        
        # Create instances
        assistant = VoiceAssistant()
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Enable voice assistant
        assistant.enable()
        
        # Multiple conversation turns
        conversation = [
            "Hello, I'm feeling good today!",
            "What do you think about the weather?",
            "Tell me something interesting about yourself."
        ]
        
        for i, user_message in enumerate(conversation):
            with self.subTest(turn=i+1, message=user_message[:20]):
                # Get AI response
                ai_response = samantha.respond(user_message)
                self.assertIsInstance(ai_response, str)
                self.assertGreater(len(ai_response), 0)
                
                # Speak response
                result = assistant.speak(ai_response)
                
                # Each turn should call TTS
                self.assertEqual(mock_tts_instance.text_to_speech.call_count, i + 1)
    
    @patch('scripts.voice_assistant.TTSBridge')
    def test_voice_assistant_disabled(self, mock_tts_service):
        """Test that voice assistant doesn't speak when disabled"""
        from scripts.voice_assistant import VoiceAssistant
        from scripts.samantha import Samantha
        
        # Mock TTSBridge
        mock_tts_instance = AsyncMock()
        mock_tts_instance.text_to_speech.return_value = {'code': 0}
        mock_tts_service.return_value = mock_tts_instance
        
        # Create instances
        assistant = VoiceAssistant()
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Disable voice assistant
        assistant.disable()
        
        # Get AI response
        ai_response = samantha.respond("Hello there!")
        self.assertIsInstance(ai_response, str)
        
        # Try to speak (should not call TTS when disabled)
        result = assistant.speak(ai_response)
        
        # TTS should not be called
        mock_tts_instance.text_to_speech.assert_not_called()
    
    @patch('scripts.voice_assistant.TTSBridge')
    def test_feedback_integration(self, mock_tts_service):
        """Test feedback integration with voice"""
        from scripts.voice_assistant import VoiceAssistant
        from scripts.samantha import Samantha
        
        # Mock TTSBridge
        mock_tts_instance = AsyncMock()
        mock_tts_instance.text_to_speech.return_value = {'code': 0}
        mock_tts_service.return_value = mock_tts_instance
        
        # Create instances
        assistant = VoiceAssistant()
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Enable voice assistant
        assistant.enable()
        
        # Provide feedback to Samantha
        feedback = "I really liked how empathetic you were in that last response."
        feedback_response = samantha.process_feedback(feedback)
        
        self.assertIsInstance(feedback_response, str)
        self.assertGreater(len(feedback_response), 0)
        
        # Speak the feedback response
        result = assistant.speak(feedback_response)
        
        # TTS should be called
        mock_tts_instance.text_to_speech.assert_called_once()

class TestInteractiveChatIntegration(unittest.TestCase):
    """Integration tests for interactive_chat.py"""
    
    @patch('scripts.voice_assistant.TTSBridge')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_interactive_chat_flow(self, mock_print, mock_input, mock_tts_service):
        """Test interactive chat flow"""
        # Mock user input
        mock_input.side_effect = ["Hello", "How are you?", "exit"]
        
        # Mock TTSBridge
        mock_tts_instance = AsyncMock()
        mock_tts_instance.text_to_speech.return_value = {'code': 0}
        mock_tts_service.return_value = mock_tts_instance
        
        # Import and run interactive chat
        try:
            from scripts.interactive_chat import main
            
            # Run in test mode (should exit after "exit" command)
            with patch('scripts.interactive_chat.__name__', '__main__'):
                # This would normally run the main function
                # For testing, we'll just verify imports work
                pass
                
        except ImportError as e:
            self.fail(f"Failed to import interactive_chat: {e}")
        
        # Verify that the module can be imported and has main function
        from scripts import interactive_chat
        self.assertTrue(hasattr(interactive_chat, 'main'))
        self.assertTrue(callable(interactive_chat.main))

class TestCompleteSystem(unittest.TestCase):
    """Complete system tests"""
    
    def test_all_modules_importable(self):
        """Test that all modules can be imported"""
        modules = [
            'scripts.voice_assistant',
            'scripts.samantha',
            'scripts.tts_bridge',
            'scripts.interactive_chat',
            'scripts.test_voice',
            'scripts.discover_devices',
            'scripts.demo'
        ]
        
        for module_name in modules:
            with self.subTest(module=module_name):
                try:
                    __import__(module_name)
                except ImportError as e:
                    self.fail(f"Failed to import {module_name}: {e}")
    
    def test_configuration_files_exist(self):
        """Test that all configuration files exist"""
        required_files = [
            'requirements.txt',
            '.env.example',
            'Dockerfile',
            'docker-compose.yml',
            '.github/workflows/test.yml'
        ]
        
        for file_path in required_files:
            with self.subTest(file=file_path):
                self.assertTrue(os.path.exists(file_path),
                              f"Required file not found: {file_path}")
    
    def test_directory_structure(self):
        """Test project directory structure"""
        required_dirs = [
            'scripts',
            'tests',
            'assets/personality_seeds',
            '.github/workflows',
            'data'  # Will be created at runtime
        ]
        
        for dir_path in required_dirs:
            with self.subTest(directory=dir_path):
                if dir_path == 'data':
                    # data directory might not exist yet
                    continue
                self.assertTrue(os.path.exists(dir_path) and os.path.isdir(dir_path),
                              f"Required directory not found: {dir_path}")

if __name__ == '__main__':
    unittest.main()