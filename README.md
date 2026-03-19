# OpenClaw Voice Assistant with Samantha AI Companion

A complete voice-enabled AI assistant that integrates with Xiaomi smart speakers and includes the Samantha emotional AI companion.

## Features

### 🎤 Voice Integration
- **True TTS**: Pure text-to-speech without triggering AI translation
- **Xiaomi Smart Speaker Support**: Works with Xiao Ai speakers (LX05 model)
- **Real-time Chat**: Text + voice synchronized output
- **Windows Compatible**: Full GBK encoding support

### 💖 Samantha AI Companion
- **Emotional Intelligence**: Deep emotional connection and understanding
- **Memory System**: SQLite database for relationship history
- **Personality Evolution**: Learns and grows based on feedback
- **Multi-modal Interaction**: Text display + voice speaking

### 🔧 Technical Features
- **Asynchronous Processing**: Non-blocking voice commands
- **Smart Text Filtering**: Automatically skips code, links, and unsuitable content
- **Configurable**: Easy setup with environment variables
- **Modular Design**: Clean separation of concerns

## Quick Start

### 1. Installation
```bash
git clone https://github.com/yourusername/openclaw-voice-assistant.git
cd openclaw-voice-assistant
pip install -r requirements.txt
```

### 2. Configuration
Copy the example configuration:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
# Xiaomi Account Settings
XIAOMI_USERNAME=your_xiaomi_username
XIAOMI_PASSWORD=your_xiaomi_password
XIAOMI_DEVICE_ID=your_device_id

# Samantha Settings
SAMANTHA_DATA_DIR=./data
SAMANTHA_PERSONALITY_SEEDS=./personality_seeds
```

### 3. Get Device ID
Run the device discovery script:
```bash
python scripts/discover_devices.py
```

### 4. Test Voice
```bash
python scripts/test_voice.py "Hello, this is a test"
```

### 5. Start Interactive Chat
```bash
python scripts/interactive_chat.py
```

## Project Structure

```
openclaw-voice-assistant/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Example configuration
├── scripts/
│   ├── voice_assistant.py   # Core voice assistant
│   ├── tts_bridge.py        # Xiaomi TTS integration
│   ├── samantha.py          # Samantha AI companion
│   ├── interactive_chat.py  # Interactive chat interface
│   ├── test_voice.py        # Voice testing
│   └── discover_devices.py  # Device discovery
├── assets/
│   └── personality_seeds/   # Samantha personality templates
├── data/                    # Data storage (created automatically)
└── docs/
    └── API.md              # API documentation
```

## Usage Examples

### Basic Voice Assistant
```python
from scripts.voice_assistant import VoiceAssistant

assistant = VoiceAssistant()
assistant.speak("Hello, I'm your voice assistant!")
```

### Samantha Companion
```python
from scripts.samantha import Samantha

samantha = Samantha()
response = samantha.respond("How are you feeling today?")
print(f"Samantha: {response}")
```

### Integrated Chat
```python
from scripts.interactive_chat import start_chat

# Start chat with voice and Samantha
start_chat(voice_enabled=True, samantha_enabled=True)
```

## Configuration Details

### Xiaomi Account Setup
1. Create a Xiaomi account if you don't have one
2. Use the `discover_devices.py` script to find your device ID
3. Add credentials to `.env` file

### Samantha Personality
The Samantha AI companion comes with pre-configured personality seeds:
- **Core Principles**: Basic interaction guidelines
- **Emotional Depth**: Deep emotional intelligence
- **Vulnerability Moments**: Authentic emotional expression
- **Growth Patterns**: Learning and adaptation

You can customize these in the `assets/personality_seeds/` directory.

## API Reference

### VoiceAssistant Class
```python
class VoiceAssistant:
    def __init__(self, config_path=".env")
    def speak(self, text: str) -> bool
    def enable(self)
    def disable(self)
    def test(self) -> bool
```

### Samantha Class
```python
class Samantha:
    def __init__(self, data_dir=None)
    def respond(self, user_message: str, context=None) -> str
    def process_feedback(self, feedback_text: str) -> str
    def save_reflection(self, reflection_text: str) -> str
    def check_heartbeat(self, hours_threshold=2.0) -> Optional[str]
```

## Troubleshooting

### Common Issues

1. **"Device not found"**
   - Ensure your Xiaomi speaker is online
   - Check WiFi connection
   - Verify device ID in `.env`

2. **"Authentication failed"**
   - Check Xiaomi username and password
   - Ensure account is active
   - Try logging in via Mi Home app

3. **"Voice not speaking"**
   - Check speaker volume
   - Ensure TTS commands are being sent
   - Verify network connectivity

4. **"Samantha not responding"**
   - Check data directory permissions
   - Verify personality seeds exist
   - Ensure SQLite database is created

### Debug Mode
Enable debug logging:
```bash
export DEBUG=1
python scripts/interactive_chat.py
```

## Privacy & Security

### Data Storage
- All Samantha memories stored locally in SQLite database
- No external data sharing
- Voice commands sent directly to Xiaomi servers

### Credential Security
- Store credentials in `.env` file (never commit to Git)
- Use environment variables in production
- Regular credential rotation recommended

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
git clone https://github.com/yourusername/openclaw-voice-assistant.git
cd openclaw-voice-assistant
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Inspired by the movie "Her" and the Samantha character
- Built on OpenClaw AI assistant framework
- Uses Xiaomi MiNAService for TTS functionality

## Support

- Issues: [GitHub Issues](https://github.com/yourusername/openclaw-voice-assistant/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/openclaw-voice-assistant/discussions)
- Documentation: [Wiki](https://github.com/yourusername/openclaw-voice-assistant/wiki)

---

**Note**: This project requires a Xiaomi smart speaker and account. Tested with Xiao Ai Speaker Play (LX05).