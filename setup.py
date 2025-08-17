#!/usr/bin/env python3
"""
Setup script for Drowsiness Detection Project
"""

import subprocess
import sys
import os

def install_requirements():
    """Install all required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def download_landmarks():
    """Download facial landmarks file"""
    print("Downloading facial landmarks file...")
    try:
        subprocess.check_call([sys.executable, "download_landmarks.py"])
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading landmarks file: {e}")
        return False

def main():
    print("🚀 Setting up Drowsiness Detection Project...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation!")
        return False
    
    # Download landmarks file
    if not download_landmarks():
        print("❌ Setup failed during landmarks file download!")
        return False
    
    print("=" * 50)
    print("✅ Setup completed successfully!")
    print("\nTo run the drowsiness detector:")
    print("python drowsiness_detector.py")
    print("\nPress 'q' to quit the application when running.")
    
    return True

if __name__ == "__main__":
    main() 