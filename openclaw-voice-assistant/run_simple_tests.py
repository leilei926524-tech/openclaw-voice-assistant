#!/usr/bin/env python3
"""
Simple test runner for OpenClaw Voice Assistant
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    modules_to_test = [
        'scripts.voice_assistant',
        'scripts.samantha',
        'scripts.tts_bridge',
        'scripts.interactive_chat',
        'scripts.test_voice',
        'scripts.discover_devices',
        'scripts.demo'
    ]
    
    success_count = 0
    fail_count = 0
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
            success_count += 1
        except ImportError as e:
            print(f"  ❌ {module_name}: {e}")
            fail_count += 1
    
    return success_count, fail_count

def test_file_existence():
    """Test that required files exist"""
    print("\nTesting file existence...")
    
    required_files = [
        'requirements.txt',
        '.env.example',
        'README.md',
        'LICENSE',
        'Dockerfile',
        'docker-compose.yml',
        '.github/workflows/test.yml'
    ]
    
    success_count = 0
    fail_count = 0
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
            success_count += 1
        else:
            print(f"  ❌ {file_path} (not found)")
            fail_count += 1
    
    return success_count, fail_count

def test_directory_structure():
    """Test directory structure"""
    print("\nTesting directory structure...")
    
    required_dirs = [
        'scripts',
        'tests',
        'assets/personality_seeds',
        '.github/workflows'
    ]
    
    success_count = 0
    fail_count = 0
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print(f"  ✅ {dir_path}/")
            success_count += 1
        else:
            print(f"  ❌ {dir_path}/ (not found)")
            fail_count += 1
    
    return success_count, fail_count

def test_requirements_file():
    """Test requirements.txt format"""
    print("\nTesting requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        
        dependencies = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
        
        if len(dependencies) > 0:
            print(f"  ✅ Found {len(dependencies)} dependencies")
            
            # Check for key dependencies
            key_deps = ['miservice', 'aiohttp']
            found_key_deps = []
            
            for dep in dependencies:
                for key_dep in key_deps:
                    if key_dep in dep.lower():
                        found_key_deps.append(key_dep)
            
            if found_key_deps:
                print(f"  ✅ Found key dependencies: {', '.join(found_key_deps)}")
            else:
                print(f"  ⚠️  Missing some key dependencies")
            
            return 1, 0
        else:
            print("  ❌ No dependencies found in requirements.txt")
            return 0, 1
            
    except Exception as e:
        print(f"  ❌ Error reading requirements.txt: {e}")
        return 0, 1

def test_env_example():
    """Test .env.example format"""
    print("\nTesting .env.example...")
    
    try:
        with open('.env.example', 'r') as f:
            content = f.read()
        
        # Check for required variables
        required_vars = ['XIAOMI_USERNAME', 'XIAOMI_PASSWORD', 'XIAOMI_DEVICE_ID']
        missing_vars = []
        
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
        
        if not missing_vars:
            print(f"  ✅ All required variables found in .env.example")
            return 1, 0
        else:
            print(f"  ❌ Missing variables in .env.example: {', '.join(missing_vars)}")
            return 0, 1
            
    except Exception as e:
        print(f"  ❌ Error reading .env.example: {e}")
        return 0, 1

def main():
    """Main function"""
    print("OpenClaw Voice Assistant - Simple Test Runner")
    print("=" * 60)
    
    total_success = 0
    total_fail = 0
    
    # Run tests
    success, fail = test_imports()
    total_success += success
    total_fail += fail
    
    success, fail = test_file_existence()
    total_success += success
    total_fail += fail
    
    success, fail = test_directory_structure()
    total_success += success
    total_fail += fail
    
    success, fail = test_requirements_file()
    total_success += success
    total_fail += fail
    
    success, fail = test_env_example()
    total_success += success
    total_fail += fail
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  Total tests: {total_success + total_fail}")
    print(f"  Passed: {total_success}")
    print(f"  Failed: {total_fail}")
    
    if total_fail == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_fail} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())