import os
import sys
import platform
import subprocess

def create_virtualenv():
    """Create a virtual environment."""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    print("Virtual environment created.")

def activate_virtualenv():
    """Activate the virtual environment based on the operating system."""
    os_type = platform.system().lower()
    activate_script = ""

    if os_type == "windows":
        activate_script = os.path.join("venv", "Scripts", "activate")
    else:
        activate_script = os.path.join("venv", "bin", "activate")

    if not os.path.exists(activate_script):
        print("Error: Activation script not found. Ensure the virtual environment was created correctly.")
        sys.exit(1)

    print(f"To activate the virtual environment, run:")
    if os_type == "windows":
        print(f"    {activate_script}")
    else:
        print(f"    source {activate_script}")

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    print("Dependencies installed.")

def main():
    try:
        create_virtualenv()
        activate_virtualenv()
        install_dependencies()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()