# Quick Start Guide

Get up and running with OpenClaw Voice Assistant in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- Xiaomi smart speaker (tested with Xiao Ai Speaker Play LX05)
- Xiaomi account (phone number or email)

## Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/openclaw-voice-assistant.git
cd openclaw-voice-assistant

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your credentials
# You'll need:
# - Xiaomi username (phone number or email)
# - Xiaomi password
# - Device ID (discover in next step)
```

## Step 3: Discover Your Device

```bash
# Run device discovery
python scripts/discover_devices.py

# This will show your devices. Copy the Device ID.
# Example output:
# Found 1 device(s):
# 1. Xiao Ai Speaker Play (LX05)
#    Status: ✓ Online
#    Device ID: 32647872-4ffc-4288-9288-fe6d6369fed4
```

## Step 4: Update Configuration

Edit your `.env` file:

```env
XIAOMI_USERNAME=your_phone_number_or_email
XIAOMI_PASSWORD=your_password
XIAOMI_DEVICE_ID=your_device_id_from_discovery
```

## Step 5: Test Voice

```bash
# Run comprehensive test
python scripts/test_voice.py

# Or test a simple message
python scripts/tts_bridge.py --speak "Hello, this is a test"
```

## Step 6: Start Interactive Chat

```bash
# Start chat with voice and Samantha
python scripts/interactive_chat.py

# Or start without voice
python scripts/interactive_chat.py --no-voice

# Or start without Samantha
python scripts/interactive_chat.py --no-samantha
```

## Step 7: Use in Your Code

```python
from scripts.voice_assistant import VoiceAssistant

# Initialize
assistant = VoiceAssistant()

# Speak text
assistant.speak("Hello, I'm your voice assistant!")

# Check if speaking
if assistant.is_speaking():
    print("Currently speaking...")
    assistant.wait_until_done()

# Test connection
result = assistant.test()
if result["success"]:
    print("Voice assistant is working!")
```

## Troubleshooting

### Common Issues

1. **"Authentication failed"**
   - Check username/password in .env
   - Verify account is active
   - Try logging in via Mi Home app

2. **"Device not found"**
   - Run `python scripts/discover_devices.py` to verify device ID
   - Ensure speaker is online
   - Check WiFi connection

3. **"Voice not speaking"**
   - Check speaker volume
   - Verify TTS commands are being sent
   - Run `python scripts/test_voice.py` for diagnostics

4. **"Import errors"**
   - Ensure you're in the project directory
   - Check Python version (3.8+ required)
   - Verify all dependencies installed

### Quick Fixes

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear cache
rm -rf __pycache__/

# Reset configuration
rm .env
cp .env.example .env
# Edit .env again
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore [scripts/](scripts/) directory for more examples
- Check out Samantha's [personality seeds](assets/personality_seeds/) for customization
- Join the community for support and updates

## Need Help?

- Check the [troubleshooting section](#troubleshooting)
- Review the [README.md](README.md) documentation
- Open an issue on GitHub
- Join the community discussions

---

**Congratulations!** You now have a working voice assistant with Samantha AI companion. 🎤