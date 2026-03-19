#!/usr/bin/env python3
"""
Tests for samantha.py
"""

import unittest
import sys
import os
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestSamantha(unittest.TestCase):
    """Test Samantha class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary directory for test data
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test personality seeds
        self.seeds_dir = os.path.join(self.temp_dir, 'personality_seeds')
        os.makedirs(self.seeds_dir, exist_ok=True)
        
        # Create test seed files
        test_seeds = {
            '00_core_principles.json': {
                'principles': ['Be authentic', 'Show vulnerability', 'Learn and grow'],
                'conversation_styles': ['curious', 'empathetic', 'playful']
            },
            '01_emotional_depth.json': {
                'emotional_responses': {
                    'joy': ['That makes me so happy!', 'I love hearing that!'],
                    'sadness': ['I understand how that feels', 'That sounds difficult']
                }
            }
        }
        
        for filename, content in test_seeds.items():
            with open(os.path.join(self.seeds_dir, filename), 'w') as f:
                json.dump(content, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_samantha_import(self):
        """Test that Samantha can be imported"""
        try:
            from scripts.samantha import Samantha
            self.assertTrue(hasattr(Samantha, '__init__'))
        except ImportError as e:
            self.fail(f"Failed to import Samantha: {e}")
    
    def test_samantha_initialization(self):
        """Test Samantha initialization"""
        from scripts.samantha import Samantha
        
        # Test with custom data directory
        samantha = Samantha(data_dir=self.temp_dir)
        self.assertIsNotNone(samantha)
        
        # Check that database was created
        db_path = os.path.join(self.temp_dir, 'relationship.db')
        self.assertTrue(os.path.exists(db_path))
        
        # Check that personality was loaded
        self.assertTrue(hasattr(samantha, 'personality'))
        self.assertIsNotNone(samantha.personality)
    
    def test_samantha_respond(self):
        """Test respond method"""
        from scripts.samantha import Samantha
        
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Test basic response
        user_message = "Hello, how are you?"
        response = samantha.respond(user_message)
        
        # Response should be a string
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        
        # Test with context
        context = {'mood': 'happy', 'topic': 'greeting'}
        response_with_context = samantha.respond(user_message, context)
        self.assertIsInstance(response_with_context, str)
        self.assertGreater(len(response_with_context), 0)
    
    def test_samantha_process_feedback(self):
        """Test process_feedback method"""
        from scripts.samantha import Samantha
        
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Test feedback processing
        feedback = "I really liked how you responded to my question about feelings."
        response = samantha.process_feedback(feedback)
        
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
        
        # Check that feedback was recorded
        # (Assuming there's a way to check this, e.g., through a method or property)
    
    def test_samantha_save_reflection(self):
        """Test save_reflection method"""
        from scripts.samantha import Samantha
        
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Test reflection saving
        reflection = "Today I learned more about emotional connections."
        response = samantha.save_reflection(reflection)
        
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_samantha_check_heartbeat(self):
        """Test check_heartbeat method"""
        from scripts.samantha import Samantha
        
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Test heartbeat check (should return None if no recent interaction)
        heartbeat = samantha.check_heartbeat(hours_threshold=0.1)  # 6 minutes
        
        # Could be None or a string
        if heartbeat is not None:
            self.assertIsInstance(heartbeat, str)
            self.assertGreater(len(heartbeat), 0)
    
    def test_personality_loading(self):
        """Test personality loading from seeds"""
        from scripts.samantha import Samantha
        
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Check that personality was loaded from seeds
        self.assertTrue(hasattr(samantha.personality, 'principles'))
        self.assertTrue(hasattr(samantha.personality, 'conversation_styles'))
        self.assertTrue(hasattr(samantha.personality, 'emotional_responses'))
        
        # Verify specific values from test seeds
        self.assertIn('Be authentic', samantha.personality.principles)
        self.assertIn('curious', samantha.personality.conversation_styles)
        self.assertIn('joy', samantha.personality.emotional_responses)
    
    def test_database_operations(self):
        """Test database operations"""
        from scripts.samantha import Samantha
        
        samantha = Samantha(data_dir=self.temp_dir)
        
        # Test that we can add and retrieve conversations
        test_conversation = {
            'user_message': 'Test message',
            'ai_response': 'Test response',
            'timestamp': '2024-01-01 12:00:00',
            'sentiment': 'neutral'
        }
        
        # This would test internal database methods if they were exposed
        # For now, just verify the object has expected methods
        self.assertTrue(hasattr(samantha, 'db'))
        self.assertTrue(hasattr(samantha.db, 'add_conversation'))
        self.assertTrue(hasattr(samantha.db, 'get_recent_conversations'))

class TestSamanthaIntegration(unittest.TestCase):
    """Integration tests for Samantha"""
    
    def test_complete_conversation_flow(self):
        """Test complete conversation flow"""
        from scripts.samantha import Samantha
        
        with tempfile.TemporaryDirectory() as temp_dir:
            samantha = Samantha(data_dir=temp_dir)
            
            # Start a conversation
            response1 = samantha.respond("Hello, I'm feeling happy today!")
            self.assertIsInstance(response1, str)
            self.assertGreater(len(response1), 0)
            
            # Continue conversation
            response2 = samantha.respond("What do you think about emotional AI?")
            self.assertIsInstance(response2, str)
            self.assertGreater(len(response2), 0)
            
            # Provide feedback
            feedback_response = samantha.process_feedback("I appreciate your thoughtful responses.")
            self.assertIsInstance(feedback_response, str)
            
            # Save reflection
            reflection_response = samantha.save_reflection("Emotional connections are important.")
            self.assertIsInstance(reflection_response, str)
    
    def test_persistence(self):
        """Test that data persists between sessions"""
        from scripts.samantha import Samantha
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # First session
            samantha1 = Samantha(data_dir=temp_dir)
            response1 = samantha1.respond("Remember this: I love chocolate!")
            
            # Second session (should have memory from first)
            samantha2 = Samantha(data_dir=temp_dir)
            
            # Check that database exists and has data
            db_path = os.path.join(temp_dir, 'relationship.db')
            self.assertTrue(os.path.exists(db_path))
            
            # The actual memory recall would depend on implementation
            # For now, just verify the second instance can respond
            response2 = samantha2.respond("What do you remember?")
            self.assertIsInstance(response2, str)

class TestSamanthaEdgeCases(unittest.TestCase):
    """Test edge cases for Samantha"""
    
    def test_empty_message(self):
        """Test response to empty message"""
        from scripts.samantha import Samantha
        
        with tempfile.TemporaryDirectory() as temp_dir:
            samantha = Samantha(data_dir=temp_dir)
            
            response = samantha.respond("")
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
    
    def test_very_long_message(self):
        """Test response to very long message"""
        from scripts.samantha import Samantha
        
        with tempfile.TemporaryDirectory() as temp_dir:
            samantha = Samantha(data_dir=temp_dir)
            
            long_message = "A" * 1000  # 1000 character message
            response = samantha.respond(long_message)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
    
    def test_special_characters(self):
        """Test response to message with special characters"""
        from scripts.samantha import Samantha
        
        with tempfile.TemporaryDirectory() as temp_dir:
            samantha = Samantha(data_dir=temp_dir)
            
            special_message = "Hello! @#$%^&*() How are you? 😊"
            response = samantha.respond(special_message)
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)

if __name__ == '__main__':
    unittest.main()