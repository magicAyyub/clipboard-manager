#!/bin/bash

# Define paths
VENV_PATH="$(dirname "$0")/venv"
APP_PATH="$(dirname "$0")/clipboardApp"
PID_FILE="/tmp/clippy.pid"

case "$1" in
  run)
    echo "Starting Clippy..."
    # Navigate to the application folder
    cd "$APP_PATH" || exit 1

    # Activate the virtual environment
    source "$VENV_PATH/bin/activate"

    # Start the application in the background and save its PID
    python main.py &
    echo $! > "$PID_FILE"

    echo "Clippy is now running."
    ;;
  stop)
    echo "Stopping Clippy..."
    # Check if the PID file exists
    if [ -f "$PID_FILE" ]; then
      # Read the PID and terminate the process
      kill -9 "$(cat "$PID_FILE")"
      rm "$PID_FILE"
      echo "Clippy has been stopped."
    else
      echo "Clippy is not running."
    fi
    ;;
  *)
    echo "Usage: $0 {run|stop}"
    ;;
esac