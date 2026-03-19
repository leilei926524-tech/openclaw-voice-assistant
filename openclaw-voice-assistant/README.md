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
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: Automated testing and deployment
- **Comprehensive Testing**: Unit and integration tests

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/leilei926524-tech/openclaw-voice-assistant.git
cd openclaw-voice-assistant

# Copy and configure environment
cp .env.example .env
# Edit .env with your Xiaomi credentials

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 2: Python Installation
```bash
# Clone the repository
git clone https://github.com/leilei926524-tech/openclaw-voice-assistant.git
cd openclaw-voice-assistant

# Install dependencies
pip install -r requirements.txt

# Configuration
cp .env.example .env
# Edit .env with your settings

# Get Device ID
python scripts/discover_devices.py

# Test Voice
python scripts/test_voice.py "Hello, this is a test"

# Start Interactive Chat
python scripts/interactive_chat.py
```

### Configuration
Edit `.env` with your settings:
```env
# Xiaomi Account Settings
XIAOMI_USERNAME=your_xiaomi_username
XIAOMI_PASSWORD=your_xiaomi_password
XIAOMI_DEVICE_ID=your_device_id

# Samantha Settings
SAMANTHA_DATA_DIR=./data
SAMANTHA_PERSONALITY_SEEDS=./personality_seeds

# Application Settings
DEBUG=false
LOG_LEVEL=INFO
```

## Project Structure

```
openclaw-voice-assistant/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Example configuration
├── Dockerfile               # Docker container definition
├── docker-compose.yml       # Docker Compose configuration
├── scripts/
│   ├── voice_assistant.py   # Core voice assistant
│   ├── tts_bridge.py        # Xiaomi TTS integration
│   ├── samantha.py          # Samantha AI companion
│   ├── interactive_chat.py  # Interactive chat interface
│   ├── test_voice.py        # Voice testing
│   └── discover_devices.py  # Device discovery
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_basic.py       # Basic tests
├── .github/workflows/       # CI/CD pipelines
│   └── test.yml            # Automated testing
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

## Development

### Development Setup
```bash
# Clone repository
git clone https://github.com/leilei926524-tech/openclaw-voice-assistant.git
cd openclaw-voice-assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-cov pytest-asyncio flake8 black

# Run tests
pytest tests/ -v

# Run linting
flake8 scripts/ --max-line-length=127

# Format code
black scripts/
```

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=scripts --cov-report=html

# Run specific test file
pytest tests/test_basic.py -v
```

### CI/CD Pipeline
The project includes GitHub Actions for:
- **Automated Testing**: Runs on every push and pull request
- **Code Quality**: Flake8 linting and security scanning
- **Coverage Reports**: Code coverage tracking
- **Weekly Scheduled Runs**: Regular maintenance checks

View workflow status at: https://github.com/leilei926524-tech/openclaw-voice-assistant/actions

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests** to ensure everything works
6. **Update documentation** if needed
7. **Submit a pull request**

### Pull Request Guidelines
- Include a clear description of changes
- Add tests for new features
- Update documentation as needed
- Ensure code passes linting and tests
- Follow the existing code style

### Code Style
- Use Black for code formatting
- Follow PEP 8 guidelines
- Maximum line length: 127 characters
- Use type hints where appropriate
- Add docstrings for public functions

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