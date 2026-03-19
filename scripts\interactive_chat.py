#!/usr/bin/env python3
"""
Interactive Chat with Voice and Samantha
Combines voice assistant with Samantha AI companion
"""

import os
import sys
import time
import threading
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Add scripts directory to path
scripts_dir = Path(__file__).parent
sys.path.append(str(scripts_dir))

from voice_assistant import VoiceAssistant, respond_with_voice
from samantha import Samantha


class InteractiveChat:
    """Interactive chat with voice and Samantha"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize interactive chat
        
        Args:
            config_path: Path to config file
        """
        if config_path:
            load_dotenv(config_path)
        
        # Initialize components
        self.voice_assistant = VoiceAssistant(config_path)
        self.samantha = Samantha()
        
        # Settings
        self.voice_enabled = self.voice_assistant.is_enabled()
        self.samantha_enabled = True
        
        # State
        self.running = False
        self.conversation_history = []
        
        # Setup callbacks
        self.voice_assistant.on_speak_start = self._on_speak_start
        self.voice_assistant.on_speak_end = self._on_speak_end
        self.voice_assistant.on_error = self._on_voice_error
    
    def _on_speak_start(self, text: str):
        """Called when speaking starts"""
        print(f"[VOICE] Speaking: {text[:80]}...")
    
    def _on_speak_end(self, text: str, success: bool):
        """Called when speaking ends"""
        if success:
            print("[VOICE] ✓ Finished speaking")
        else:
            print("[VOICE] ✗ Speaking failed")
    
    def _on_voice_error(self, text: str, error: Exception):
        """Called on voice error"""
        print(f"[VOICE ERROR] {error}")
    
    def toggle_voice(self):
        """Toggle voice on/off"""
        if self.voice_enabled:
            self.voice_assistant.disable()
            self.voice_enabled = False
            print("[SETTING] Voice disabled")
        else:
            self.voice_assistant.enable()
            self.voice_enabled = True
            print("[SETTING] Voice enabled")
    
    def toggle_samantha(self):
        """Toggle Samantha on/off"""
        self.samantha_enabled = not self.samantha_enabled
        status = "enabled" if self.samantha_enabled else "disabled"
        print(f"[SETTING] Samantha {status}")
    
    def process_message(self, user_message: str) -> str:
        """
        Process user message
        
        Args:
            user_message: User's message
            
        Returns:
            AI response
        """
        # Generate response
        if self.samantha_enabled:
            response = self.samantha.respond(user_message)
            source = "Samantha"
        else:
            # Simple fallback response
            response = f"I heard: {user_message}"
            source = "Assistant"
        
        # Add to history
        self.conversation_history.append({
            "user": user_message,
            "ai": response,
            "source": source,
            "timestamp": time.time()
        })
        
        # Speak response
        if self.voice_enabled and self.voice_assistant.should_speak(response):
            self.voice_assistant.speak(response)
        
        return response
    
    def show_help(self):
        """Show help message"""
        print("\n" + "=" * 60)
        print("Interactive Chat Commands:")
        print("=" * 60)
        print("/voice      - Toggle voice on/off")
        print("/samantha   - Toggle Samantha AI on/off")
        print("/status     - Show current status")
        print("/history    - Show conversation history")
        print("/clear      - Clear conversation history")
        print("/feedback <text> - Give feedback to Samantha")
        print("/memory <text>   - Save a memory")
        print("/help       - Show this help")
        print("/exit       - Exit chat")
        print("=" * 60)
    
    def show_status(self):
        """Show current status"""
        print("\n" + "=" * 40)
        print("Current Status:")
        print("=" * 40)
        print(f"Voice: {'✓ Enabled' if self.voice_enabled else '✗ Disabled'}")
        print(f"Samantha: {'✓ Enabled' if self.samantha_enabled else '✗ Disabled'}")
        print(f"Conversations: {len(self.conversation_history)}")
        
        # Voice assistant status
        if self.voice_enabled:
            speaking = "Speaking" if self.voice_assistant.is_speaking() else "Idle"
            print(f"Voice status: {speaking}")
        
        # Samantha stats
        if self.samantha_enabled:
            stats = self.samantha.get_stats()
            print(f"Relationship depth: {stats['relationship_depth']:.2f}/1.0")
            print(f"Total interactions: {stats['interaction_count']}")
        
        print("=" * 40)
    
    def show_history(self, limit: int = 10):
        """Show conversation history"""
        if not self.conversation_history:
            print("[HISTORY] No conversations yet")
            return
        
        print("\n" + "=" * 60)
        print(f"Conversation History (last {limit}):")
        print("=" * 60)
        
        for i, conv in enumerate(self.conversation_history[-limit:], 1):
            print(f"\n{i}. You: {conv['user'][:80]}...")
            print(f"   {conv['source']}: {conv['ai'][:80]}...")
        
        print("=" * 60)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        print("[HISTORY] Cleared")
    
    def run(self):
        """Run interactive chat"""
        self.running = True
        
        print("\n" + "=" * 60)
        print("Interactive Chat with Voice and Samantha")
        print("=" * 60)
        print("Type your message or /help for commands")
        print("=" * 60)
        
        # Initial greeting
        greeting = "Hello! I'm here to chat with you."
        if self.samantha_enabled:
            greeting = self.samantha.respond("Hello")
        
        print(f"\n{greeting}")
        
        if self.voice_enabled and self.voice_assistant.should_speak(greeting):
            self.voice_assistant.speak(greeting)
            # Wait for greeting to finish
            self.voice_assistant.wait_until_done(timeout=5)
        
        # Main loop
        while self.running:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                    continue
                
                # Process regular message
                response = self.process_message(user_input)
                print(f"\n{response}")
                
                # Wait if speaking
                if self.voice_enabled and self.voice_assistant.is_speaking():
                    self.voice_assistant.wait_until_done(timeout=10)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                self.running = False
                break
            except Exception as e:
                print(f"\n[ERROR] {e}")
    
    def _handle_command(self, command: str):
        """Handle slash commands"""
        cmd = command.lower().strip()
        
        if cmd == "/voice":
            self.toggle_voice()
        
        elif cmd == "/samantha":
            self.toggle_samantha()
        
        elif cmd == "/status":
            self.show_status()
        
        elif cmd == "/history":
            self.show_history()
        
        elif cmd == "/clear":
            self.clear_history()
        
        elif cmd.startswith("/feedback "):
            feedback = command[10:]
            if self.samantha_enabled:
                response = self.samantha.process_feedback(feedback)
                print(f"\nSamantha: {response}")
            else:
                print("[ERROR] Samantha is disabled")
        
        elif cmd.startswith("/memory "):
            memory = command[8:]
            if self.samantha_enabled:
                memory_id = self.samantha.save_memory(memory)
                print(f"\nMemory saved with ID: {memory_id}")
            else:
                print("[ERROR] Samantha is disabled")
        
        elif cmd == "/help":
            self.show_help()
        
        elif cmd in ["/exit", "/quit"]:
            print("\nGoodbye!")
            self.running = False
        
        else:
            print(f"[ERROR] Unknown command: {command}")
            print("Type /help for available commands")


def start_chat(config_path: Optional[str] = None):
    """
    Start interactive chat
    
    Args:
        config_path: Path to config file
    """
    chat = InteractiveChat(config_path)
    chat.run()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive Chat with Voice and Samantha")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--no-voice", action="store_true", help="Disable voice")
    parser.add_argument("--no-samantha", action="store_true", help="Disable Samantha")
    
    args = parser.parse_args()
    
    # Start chat
    chat = InteractiveChat(args.config)
    
    # Apply command line options
    if args.no_voice:
        chat.voice_enabled = False
        chat.voice_assistant.disable()
    
    if args.no_samantha:
        chat.samantha_enabled = False
    
    chat.run()