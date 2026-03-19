#!/usr/bin/env python3
"""
Basic tests for OpenClaw Voice Assistant
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestBasicSetup(unittest.TestCase):
    """Test basic project setup"""
    
    def test_requirements_file_exists(self):
        """Test that requirements.txt exists"""
        self.assertTrue(os.path.exists('requirements.txt'))
    
    def test_readme_exists(self):
        """Test that README.md exists"""
        self.assertTrue(os.path.exists('README.md'))
    
    def test_env_example_exists(self):
        """Test that .env.example exists"""
        self.assertTrue(os.path.exists('.env.example'))
    
    def test_scripts_directory_exists(self):
        """Test that scripts directory exists"""
        self.assertTrue(os.path.exists('scripts'))
        self.assertTrue(os.path.isdir('scripts'))
    
    def test_license_exists(self):
        """Test that LICENSE exists"""
        self.assertTrue(os.path.exists('LICENSE'))

class TestScriptImports(unittest.TestCase):
    """Test that scripts can be imported"""
    
    def test_import_voice_assistant(self):
        """Test importing voice_assistant"""
        try:
            from scripts import voice_assistant
            self.assertTrue(hasattr(voice_assistant, 'VoiceAssistant'))
        except ImportError as e:
            self.fail(f"Failed to import voice_assistant: {e}")
    
    def test_import_samantha(self):
        """Test importing samantha"""
        try:
            from scripts import samantha
            self.assertTrue(hasattr(samantha, 'Samantha'))
        except ImportError as e:
            self.fail(f"Failed to import samantha: {e}")
    
    def test_import_tts_bridge(self):
        """Test importing tts_bridge"""
        try:
            from scripts import tts_bridge
            self.assertTrue(hasattr(tts_bridge, 'TTSService'))
        except ImportError as e:
            self.fail(f"Failed to import tts_bridge: {e}")

class TestConfiguration(unittest.TestCase):
    """Test configuration files"""
    
    def test_requirements_format(self):
        """Test that requirements.txt has valid format"""
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        
        # Check for common dependencies
        dependencies = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        # Should have at least some dependencies
        self.assertGreater(len(dependencies), 0)
        
        # Check for expected dependencies
        expected_deps = ['miservice', 'aiohttp', 'asyncio']
        found_deps = []
        for dep in expected_deps:
            for line in dependencies:
                if dep in line.lower():
                    found_deps.append(dep)
                    break
        
        self.assertGreater(len(found_deps), 0, f"Expected at least one of {expected_deps} in requirements.txt")

if __name__ == '__main__':
    unittest.main()