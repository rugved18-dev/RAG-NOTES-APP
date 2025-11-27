#!/usr/bin/env python
"""Setup script for Chat with Your Notes application."""
import os
import sys
import subprocess
from pathlib import Path

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists() and env_example_path.exists():
        print("Creating .env file from .env.example...")
        with open(env_example_path, "r") as src:
            with open(env_path, "w") as dst:
                dst.write(src.read())
        print("✅ .env file created. Please add your OpenAI API key.")
    elif env_path.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️  .env.example not found")

def create_uploads_directory():
    """Create uploads directory if it doesn't exist."""
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        uploads_dir.mkdir()
        print("✅ Created uploads directory")
    else:
        print("✅ Uploads directory exists")

def install_dependencies():
    """Install required Python packages."""
    print("\nInstalling dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Dependencies installed")

def main():
    """Run setup process."""
    print("🚀 Setting up Chat with Your Notes Application\n")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected\n")
    
    # Create directories
    create_uploads_directory()
    create_env_file()
    
    # Install dependencies
    install_dependencies()
    
    print("\n" + "="*50)
    print("✅ Setup Complete!")
    print("="*50)
    print("\n📋 Next Steps:")
    print("1. Edit .env and add your OpenAI API key")
    print("   OPENAI_API_KEY=sk-...your-key-here...")
    print("\n2. Run the application:")
    print("   streamlit run app/app.py")
    print("\n3. Open http://localhost:8501 in your browser")
    print("\n💡 Need an API key? Get one at:")
    print("   https://platform.openai.com/api-keys")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
