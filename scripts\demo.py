#!/usr/bin/env python3
"""
Demo script showing all features
"""

import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.voice_assistant import VoiceAssistant
from scripts.samantha import Samantha
from scripts.interactive_chat import InteractiveChat


def demo_voice_assistant():
    """Demo voice assistant features"""
    print("\n" + "=" * 60)
    print("Voice Assistant Demo")
    print("=" * 60)
    
    assistant = VoiceAssistant()
    
    # Test connection
    print("1. Testing connection...")
    result = assistant.test()
    
    if result["success"]:
        print("   ✓ Connection successful")
    else:
        print("   ✗ Connection failed")
        return False
    
    # Test speaking
    print("\n2. Testing TTS...")
    test_messages = [
        "Hello, this is a voice assistant demo",
        "I can speak different types of content",
        "But I skip code and URLs automatically"
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"   {i}. Speaking: '{msg}'")
        if assistant.speak(msg):
            assistant.wait_until_done(timeout=5)
            print("     ✓ Success")
        else:
            print("     ✗ Failed")
    
    # Test text filtering
    print("\n3. Testing text filtering...")
    test_cases = [
        ("Normal text that should be spoken", True),
        ("Short", False),  # Too short
        ("Code: `print('hello')` should not be spoken", False),
        ("URL: https://example.com should not be spoken", False),
        ("This is a longer message that contains both speakable content and some `code`", False)
    ]
    
    for text, should_speak in test_cases:
        result = assistant.should_speak(text)
        status = "✓" if result == should_speak else "✗"
        print(f"   {status} '{text[:30]}...' -> {'Speak' if result else 'Skip'}")
    
    return True


def demo_samantha():
    """Demo Samantha AI companion"""
    print("\n" + "=" * 60)
    print("Samantha AI Companion Demo")
    print("=" * 60)
    
    samantha = Samantha()
    
    # Show initial stats
    print("1. Initial statistics:")
    stats = samantha.get_stats()
    print(f"   Conversations: {stats['conversations']}")
    print(f"   Relationship depth: {stats['relationship_depth']:.2f}/1.0")
    
    # Test conversation
    print("\n2. Test conversation:")
    test_messages = [
        "Hello Samantha",
        "How are you feeling today?",
        "I've been thinking about our conversations"
    ]
    
    for msg in test_messages:
        print(f"   You: {msg}")
        response = samantha.respond(msg)
        print(f"   Samantha: {response}")
        time.sleep(1)
    
    # Test feedback
    print("\n3. Test feedback:")
    feedback = "I like when you're thoughtful like that"
    response = samantha.process_feedback(feedback)
    print(f"   Feedback: {feedback}")
    print(f"   Samantha: {response}")
    
    # Show updated stats
    print("\n4. Updated statistics:")
    stats = samantha.get_stats()
    print(f"   Conversations: {stats['conversations']}")
    print(f"   Relationship depth: {stats['relationship_depth']:.2f}/1.0")
    print(f"   Total interactions: {stats['interaction_count']}")
    
    return True


def demo_integrated_chat():
    """Demo integrated chat"""
    print("\n" + "=" * 60)
    print("Integrated Chat Demo")
    print("=" * 60)
    
    print("Starting integrated chat with voice and Samantha...")
    print("(This will run a short automated conversation)")
    
    chat = InteractiveChat()
    
    # Disable voice for demo (to avoid actual speaking during demo)
    chat.voice_enabled = False
    chat.voice_assistant.disable()
    
    # Run automated conversation
    demo_conversation = [
        "Hello",
        "How does this integrated chat work?",
        "That sounds interesting. Can you tell me more about Samantha?",
        "Thank you for explaining"
    ]
    
    for msg in demo_conversation:
        print(f"\nYou: {msg}")
        response = chat.process_message(msg)
        print(f"Response: {response}")
        time.sleep(1)
    
    # Show final status
    print("\n" + "-" * 40)
    print("Demo completed!")
    print(f"Total conversations: {len(chat.conversation_history)}")
    
    return True


def main():
    """Run all demos"""
    print("OpenClaw Voice Assistant with Samantha - Full Demo")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    
    # Check if configured
    username = os.getenv("XIAOMI_USERNAME")
    if not username:
        print("Warning: Not fully configured")
        print("Some demos may not work without .env configuration")
        print("\nTo configure:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env with your credentials")
        print("3. Run scripts/discover_devices.py to get device ID")
        print("\nContinuing with limited demo...")
    
    # Run demos
    successes = []
    
    try:
        successes.append(demo_voice_assistant())
    except Exception as e:
        print(f"Voice assistant demo failed: {e}")
        successes.append(False)
    
    try:
        successes.append(demo_samantha())
    except Exception as e:
        print(f"Samantha demo failed: {e}")
        successes.append(False)
    
    try:
        successes.append(demo_integrated_chat())
    except Exception as e:
        print(f"Integrated chat demo failed: {e}")
        successes.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("Demo Summary")
    print("=" * 60)
    
    demos = ["Voice Assistant", "Samantha AI", "Integrated Chat"]
    for i, (demo, success) in enumerate(zip(demos, successes), 1):
        status = "✓ Passed" if success else "✗ Failed"
        print(f"{i}. {demo}: {status}")
    
    if all(successes):
        print("\n🎉 All demos passed! Your setup is working correctly.")
        print("\nNext steps:")
        print("1. Enable voice in .env (VOICE_ENABLED=true)")
        print("2. Run: python scripts/interactive_chat.py")
        print("3. Or integrate into your own code")
    else:
        print("\n⚠️ Some demos failed. Check configuration and try again.")
        print("\nTroubleshooting:")
        print("1. Verify .env configuration")
        print("2. Check Xiaomi account credentials")
        print("3. Ensure device is online")
        print("4. Run scripts/test_voice.py for diagnostics")


if __name__ == "__main__":
    import os
    main()