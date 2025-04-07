import os
import sys
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.start_app()

    def start_app(self):
        """Start the Tkinter application"""
        if self.process:
            self.process.terminate()  # Kill the old process if running
        self.process = subprocess.Popen([sys.executable, self.script_name])

    def on_modified(self, event):
        """Restart the app when a Python file changes"""
        if event.src_path.endswith(".py"):
            print(f"🔄 File {event.src_path} changed. Restarting...")
            self.start_app()

def watch_and_restart(script_name):
    """Monitor changes in the current directory and restart the app"""
    event_handler = RestartHandler(script_name)
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    script_name = "main.py"
    watch_and_restart(script_name)
