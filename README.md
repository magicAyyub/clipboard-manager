# Clippy: Clipboard Manager

When you copy something new, you often lose the previous text or worse when it's from a PDF then you need to translate, the text conserve the format and you need to paste and remove manually (very  annoying). Clippy is a simple clipboard manager that helps you keep track of your clipboard history and also make possible to remove the format of the text.

## Features :

- 	Clipboard Tracking: Clippy automatically saves your clipboard history.
-	Simple Commands: Use `clippy run` and `clippy stop` to control the app.
-	Remove Text Formatting: Easily paste text without formatting.
-	Cross-Platform: Works on Windows, Linux, and Mac.


## Installation

### 1. Clone the Repository (or Download ZIP)

```bash
git clone https://github.com/magicAyyub/clipboard-manager.git
cd clipboard-manager
```

### 2. Set Up the Virtual Environment

```bash
python3 setup_env.py
```


### 3. Setting Up the clippy Command

#### For Windows Users

- Add to System PATH
Copy the clippy.bat file to a directory included in your PATH. For example: `C:\Windows\System32`


- Test the Command:
Open a Command Prompt or PowerShell and type:

```bash
clippy run # start anywhere in a terminal
clippy stop # stop
```


#### For Linux/Mac Users

- Make the Script Executable
The `run_clippy.sh` file is included in the repository.

```bash
chmod +x run_clippy.sh
```


- Add to PATH:
Move the script to `/usr/local/bin/` or another directory in your PATH:

```bash
sudo mv run_clippy.sh /usr/local/bin/clippy
```

-  Test the Command:
Open a terminal and type:

```bash
clippy run # start anywhere in a terminal
clippy stop # stop
```


## Developer Notes

Folder Structure :
```bash
clipboard-manager/
├── clipboardApp/         # Main application folder
│   ├── main.py           # Core logic
├── venv/                 # Virtual environment (excluded from Git)
├── run_clippy.sh         # Script for Linux/Mac users
├── clippy.bat            # Script for Windows users
├── requirements.txt      # Python dependencies
└── README.md             # This documentation
```


With the clippy command, managing your clipboard has never been simpler! 🎉