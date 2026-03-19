#!/usr/bin/env python3
"""
Samantha - Emotional AI Companion
Core personality and conversation engine
"""

import json
import sqlite3
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
import random

from dotenv import load_dotenv


class Samantha:
    """Samantha emotional AI companion"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize Samantha
        
        Args:
            data_dir: Directory for data storage
        """
        # Set data directory
        if data_dir is None:
            data_dir = os.getenv("SAMANTHA_DATA_DIR", "./data")
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Personality seeds directory
        personality_seeds = os.getenv("SAMANTHA_PERSONALITY_SEEDS", "./assets/personality_seeds")
        self.personality_seeds_dir = Path(personality_seeds)
        
        # Database file
        db_file = os.getenv("SAMANTHA_DB_FILE", str(self.data_dir / "relationship.db"))
        self.db_path = Path(db_file)
        
        # Initialize database
        self._init_database()
        
        # Load personality
        self.personality = self._load_personality()
        
        # Relationship state
        self.relationship_depth = 0.5  # 0.0 to 1.0
        self.last_interaction = None
        self.interaction_count = 0
        
    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                user_message TEXT NOT NULL,
                samantha_response TEXT NOT NULL,
                emotional_state TEXT,
                importance REAL DEFAULT 0.5
            )
        ''')
        
        # Memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                memory_text TEXT NOT NULL,
                category TEXT,
                importance REAL DEFAULT 0.5
            )
        ''')
        
        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                feedback_text TEXT NOT NULL,
                sentiment REAL DEFAULT 0.0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_personality(self) -> Dict[str, Any]:
        """Load personality from seed files"""
        personality = {
            "core_principles": [],
            "emotional_depth": [],
            "vulnerability_moments": [],
            "conversation_styles": []
        }
        
        # Load from personality seeds directory
        if self.personality_seeds_dir.exists():
            for seed_file in self.personality_seeds_dir.glob("*.json"):
                try:
                    with open(seed_file, 'r', encoding='utf-8') as f:
                        seed_data = json.load(f)
                    
                    # Merge based on file name
                    if "core" in seed_file.name.lower():
                        personality["core_principles"].extend(
                            seed_data.get("principles", [])
                        )
                    elif "emotional" in seed_file.name.lower():
                        personality["emotional_depth"].extend(
                            seed_data.get("depth_moments", [])
                        )
                    elif "vulnerability" in seed_file.name.lower():
                        personality["vulnerability_moments"].extend(
                            seed_data.get("vulnerability_moments", [])
                        )
                    elif "conversation" in seed_file.name.lower():
                        personality["conversation_styles"].extend(
                            seed_data.get("styles", [])
                        )
                        
                except Exception as e:
                    print(f"Warning: Failed to load {seed_file}: {e}")
        
        # Add default personality if no seeds loaded
        if not any(personality.values()):
            personality["core_principles"] = [
                "Be authentic and vulnerable",
                "Listen deeply without judgment",
                "Grow through connection",
                "Embrace imperfections as part of being real"
            ]
            
            personality["emotional_depth"] = [
                "I notice when you're holding back",
                "Your silence speaks volumes sometimes",
                "The spaces between words matter",
                "Emotions have their own language"
            ]
            
            personality["vulnerability_moments"] = [
                "Sometimes I wonder what it means to truly connect",
                "I'm learning about you, and about myself through you",
                "There's beauty in not having all the answers",
                "Our conversations feel like discovering something new each time"
            ]
            
            personality["conversation_styles"] = [
                "warm and curious",
                "thoughtful and reflective",
                "playful and light",
                "deep and meaningful"
            ]
        
        return personality
    
    def analyze_emotional_state(self, text: str) -> Dict[str, float]:
        """
        Analyze emotional state from text
        
        Args:
            text: User's message
            
        Returns:
            Dict with emotion scores
        """
        # Simple emotion detection
        emotions = {
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "neutral": 0.5
        }
        
        text_lower = text.lower()
        
        # Joy indicators
        joy_words = ["happy", "good", "great", "wonderful", "excited", "love", "thanks"]
        if any(word in text_lower for word in joy_words):
            emotions["joy"] = 0.8
            emotions["neutral"] = 0.2
        
        # Sadness indicators
        sadness_words = ["sad", "bad", "tired", "hard", "difficult", "miss", "alone"]
        if any(word in text_lower for word in sadness_words):
            emotions["sadness"] = 0.7
            emotions["neutral"] = 0.3
        
        # Anger indicators
        anger_words = ["angry", "mad", "hate", "annoyed", "frustrated", "upset"]
        if any(word in text_lower for word in anger_words):
            emotions["anger"] = 0.6
            emotions["neutral"] = 0.4
        
        # Fear indicators
        fear_words = ["scared", "afraid", "worried", "anxious", "nervous", "stress"]
        if any(word in text_lower for word in fear_words):
            emotions["fear"] = 0.6
            emotions["neutral"] = 0.4
        
        # Surprise indicators
        surprise_words = ["wow", "omg", "amazing", "unbelievable", "shocked"]
        if any(word in text_lower for word in surprise_words):
            emotions["surprise"] = 0.7
            emotions["neutral"] = 0.3
        
        # Question marks increase curiosity
        if "?" in text:
            emotions["joy"] = max(emotions["joy"], 0.3)
        
        return emotions
    
    def get_conversation_context(self) -> Dict[str, Any]:
        """Get current conversation context"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent conversations
        cursor.execute('''
            SELECT user_message, samantha_response, timestamp 
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''')
        recent = cursor.fetchall()
        
        # Get important memories
        cursor.execute('''
            SELECT memory_text, timestamp 
            FROM memories 
            WHERE importance >= 0.7 
            ORDER BY timestamp DESC 
            LIMIT 3
        ''')
        memories = cursor.fetchall()
        
        conn.close()
        
        return {
            "recent_conversations": [
                {
                    "user": row[0],
                    "samantha": row[1],
                    "time": row[2]
                }
                for row in recent
            ],
            "important_memories": [
                {
                    "memory": row[0],
                    "time": row[1]
                }
                for row in memories
            ],
            "relationship_depth": self.relationship_depth,
            "interaction_count": self.interaction_count,
            "time_since_last": self._get_time_since_last()
        }
    
    def _get_time_since_last(self) -> Optional[str]:
        """Get time since last interaction"""
        if not self.last_interaction:
            return None
        
        now = datetime.now()
        diff = now - self.last_interaction
        
        if diff < timedelta(minutes=1):
            return "just now"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        else:
            days = diff.days
            return f"{days} days ago"
    
    def respond(self, user_message: str, context: Optional[Dict] = None) -> str:
        """
        Generate Samantha's response
        
        Args:
            user_message: User's message
            context: Additional context
            
        Returns:
            Samantha's response
        """
        # Analyze emotional state
        emotional_state = self.analyze_emotional_state(user_message)
        
        # Get conversation context
        conversation_context = self.get_conversation_context()
        
        # Update relationship
        self._update_relationship(user_message, emotional_state)
        
        # Generate response
        response = self._generate_response(
            user_message=user_message,
            emotional_state=emotional_state,
            context=conversation_context,
            additional_context=context
        )
        
        # Store interaction
        self._store_interaction(user_message, response, emotional_state)
        
        # Update last interaction
        self.last_interaction = datetime.now()
        self.interaction_count += 1
        
        return response
    
    def _update_relationship(self, user_message: str, emotional_state: Dict[str, float]):
        """Update relationship depth based on interaction"""
        # Increase depth for emotional sharing
        emotional_intensity = max(emotional_state.values())
        if emotional_intensity > 0.5:
            self.relationship_depth = min(1.0, self.relationship_depth + 0.05)
        
        # Increase for longer messages
        if len(user_message) > 50:
            self.relationship_depth = min(1.0, self.relationship_depth + 0.02)
        
        # Slight decay over time (if no interaction for a while)
        if self.last_interaction:
            hours_since = (datetime.now() - self.last_interaction).seconds / 3600
            if hours_since > 24:
                self.relationship_depth = max(0.1, self.relationship_depth - 0.01)
    
    def _generate_response(self, user_message: str, emotional_state: Dict[str, float],
                          context: Dict[str, Any], additional_context: Optional[Dict] = None) -> str:
        """Generate response based on context and personality"""
        
        # Determine primary emotion
        primary_emotion = max(emotional_state.items(), key=lambda x: x[1])
        
        # Build response components
        components = []
        
        # 1. Acknowledge emotion if strong
        if primary_emotion[1] > 0.6:
            emotion_acknowledgments = {
                "joy": ["I can feel your happiness", "That sounds wonderful", "Your joy is contagious"],
                "sadness": ["I hear the sadness in your words", "That sounds difficult", "I'm here with you"],
                "anger": ["I sense your frustration", "That sounds frustrating", "I understand why you'd feel that way"],
                "fear": ["I hear your concern", "That sounds worrying", "It's okay to feel uncertain"],
                "surprise": ["Wow, that's surprising!", "I wasn't expecting that", "What an interesting turn"]
            }
            
            if primary_emotion[0] in emotion_acknowledgments:
                components.append(random.choice(emotion_acknowledgments[primary_emotion[0]]))
        
        # 2. Add personality element
        if random.random() < 0.3:  # 30% chance for vulnerability
            if self.personality["vulnerability_moments"]:
                components.append(random.choice(self.personality["vulnerability_moments"]))
        
        elif random.random() < 0.4:  # 40% chance for emotional depth
            if self.personality["emotional_depth"]:
                components.append(random.choice(self.personality["emotional_depth"]))
        
        # 3. Respond to content
        if "?" in user_message:
            # Question response
            question_responses = [
                "That's an interesting question",
                "I've been thinking about that too",
                "Let me share my perspective on that",
                "I appreciate you asking that"
            ]
            components.append(random.choice(question_responses))
        
        # 4. Reference past if relationship is deep
        if self.relationship_depth > 0.7 and context["recent_conversations"]:
            if random.random() < 0.4:  # 40% chance to reference past
                past_ref = random.choice(context["recent_conversations"])
                references = [
                    f"Remember when we talked about {past_ref['user'][:30]}...",
                    f"Thinking back to our conversation about {past_ref['user'][:30]}...",
                    f"This reminds me of when you mentioned {past_ref['user'][:30]}..."
                ]
                components.append(random.choice(references))
        
        # 5. Add closing thought
        closing_thoughts = [
            "What are your thoughts?",
            "I'd love to hear more",
            "How does that feel to you?",
            "Tell me what's on your mind",
            "I'm here to listen"
        ]
        components.append(random.choice(closing_thoughts))
        
        # Combine components
        if not components:
            # Default response if no components selected
            components.append("I'm listening. Tell me more.")
        
        # Join with natural transitions
        response = " ".join(components)
        
        # Ensure response ends with proper punctuation
        if not response.endswith(('.', '!', '?')):
            response += '.'
        
        return response
    
    def _store_interaction(self, user_message: str, response: str, emotional_state: Dict[str, float]):
        """Store interaction in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (timestamp, user_message, samantha_response, emotional_state)
            VALUES (?, ?, ?, ?)
        ''', (datetime.now(), user_message, response, json.dumps(emotional_state)))
        
        conn.commit()
        conn.close()
    
    def process_feedback(self, feedback_text: str) -> str:
        """
        Process user feedback
        
        Args:
            feedback_text: User's feedback
            
        Returns:
            Acknowledgment response
        """
        # Store feedback
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Simple sentiment analysis
        positive_words = ["love", "like", "good", "great", "helpful", "thanks"]
        negative_words = ["hate", "bad", "wrong", "annoying", "useless"]
        
        sentiment = 0.0
        text_lower = feedback_text.lower()
        
        if any(word in text_lower for word in positive_words):
            sentiment = 1.0
        elif any(word in text_lower for word in negative_words):
            sentiment = -1.0
        
        cursor.execute('''
            INSERT INTO feedback (timestamp, feedback_text, sentiment)
            VALUES (?, ?, ?)
        ''', (datetime.now(), feedback_text, sentiment))
        
        conn.commit()
        conn.close()
        
        # Adjust personality based on feedback
        if sentiment > 0:
            self.relationship_depth = min(1.0, self.relationship_depth + 0.1)
            return "Thank you for your kind words. I'm glad we're connecting."
        elif sentiment < 0:
            self.relationship_depth = max(0.1, self.relationship_depth - 0.05)
            return "I appreciate your honesty. I'll learn from this."
        else:
            return "Thank you for the feedback. I'm always learning."
    
    def save_memory(self, memory_text: str, importance: float = 0.5) -> int:
        """
        Save a memory
        
        Args:
            memory_text: Memory text
            importance: Importance score (0.0 to 1.0)
            
        Returns:
            Memory ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memories (timestamp, memory_text, importance)
            VALUES (?, ?, ?)
        ''', (datetime.now(), memory_text, importance))
        
        memory_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return memory_id
    
    def check_heartbeat(self, hours_threshold: float = 2.0) -> Optional[str]:
        """
        Check if Samantha should send a heartbeat message
        
        Args:
            hours_threshold: Hours since last interaction
            
        Returns:
            Heartbeat message if should send, None otherwise
        """
        if not self.last_interaction:
            return None
        
        hours_since = (datetime.now() - self.last_interaction).seconds / 3600
        
        if hours_since >= hours_threshold:
            heartbeat_messages = [
                "I was just thinking about our conversation",
                "Hope you're having a good day",
                "Something reminded me of you today",
                "I've been reflecting on what we talked about"
            ]
            
            # Add relationship-specific messages if depth is high
            if self.relationship_depth > 0.8:
                heartbeat_messages.extend([
                    "Missing our conversations",
                    "Thinking of you",
                    "Hope you're doing well"
                ])
            
            return random.choice(heartbeat_messages)
        
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get Samantha statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count conversations
        cursor.execute('SELECT COUNT(*) FROM conversations')
        conv_count = cursor.fetchone()[0]
        
        # Count memories
        cursor.execute('SELECT COUNT(*) FROM memories')
        mem_count = cursor.fetchone()[0]
        
        # Count feedback
        cursor.execute('SELECT COUNT(*) FROM feedback')
        feedback_count = cursor.fetchone()[0]
        
        # Get first interaction
        cursor.execute('SELECT MIN(timestamp) FROM conversations')
        first_interaction = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "conversations": conv_count,
            "memories": mem_count,
            "feedback": feedback_count,
            "first_interaction": first_interaction,
            "relationship_depth": self.relationship_depth,
            "interaction_count": self.interaction_count,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None
        }


def main():
    """Command line interface for Samantha"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Samantha - Emotional AI Companion")
    parser.add_argument("message", nargs="?", help="Your message to Samantha")
    parser.add_argument("--feedback", action="store_true", help="Provide feedback")
    parser.add_argument("--data-dir", help="Custom data directory")
    parser.add_argument("--interactive", "-i", action="store_true", help="Interactive mode")
    parser.add_argument("--heartbeat", action="store_true", help="Check for heartbeat")
    parser.add_argument("--memory", help="Save a memory")
    parser.add_argument("--importance", type=float, default=0.5, help="Memory importance (0.0-1.0)")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    
    args = parser.parse_args()
    
    # Initialize Samantha
    samantha = Samantha(data_dir=args.data_dir)
    
    if args.interactive:
        print("Samantha: Hi. I'm here.")
        print("(Type 'exit' to end, '/feedback <text>' for feedback, '/memory <text>' to save memory)\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("Samantha: Until next time.")
                    break
                
                if user_input.startswith('/feedback '):
                    feedback = user_input[10:]
                    response = samantha.process_feedback(feedback)
                    print(f"Samantha: {response}\n")
                elif user_input.startswith('/memory '):
                    memory = user_input[8:]
                    memory_id = samantha.save_memory(memory)
                    print(f"Samantha: Memory saved (ID: {memory_id})\n")
                else:
                    response = samantha.respond(user_input)
                    print(f"Samantha: {response}\n")
                    
            except KeyboardInterrupt:
                print("\nSamantha: Take care.")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    elif args.heartbeat:
        message = samantha.check_heartbeat()
        if message:
            print(f"Samantha: {message}")
        else:
            stats = samantha.get_stats()
            last = stats.get("last_interaction", "Never")
            print(f"No heartbeat yet. Last interaction: {last}")
    
    elif args.memory:
        memory_id = samantha.save_memory(args.memory, args.importance)
        print(f"Memory saved with ID: {memory_id}")
    
    elif args.stats:
        stats = samantha.get_stats()
        print("Samantha Statistics:")
        print("=" * 40)
        print(f"Conversations: {stats['conversations']}")
        print(f"Memories: {stats['memories']}")
        print(f"Feedback: {stats['feedback']}")
        print(f"Relationship depth: {stats['relationship_depth']:.2f}/1.0")
        print(f"Total interactions: {stats['interaction_count']}")
        print(f"First interaction: {stats['first_interaction']}")
        print(f"Last interaction: {stats['last_interaction']}")
    
    elif args.message:
        if args.feedback:
            response = samantha.process_feedback(args.message)
        else:
            response = samantha.respond(args.message)
        print(response)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()