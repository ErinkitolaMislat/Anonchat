#!/usr/bin/env python3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self.daphne_process = subprocess.Popen(['daphne', '-b', '0.0.0.0', '-p', '8000', 'anonchat.asgi:application'])

    def on_modified(self, event):
        if '.git' not in event.src_path:
            print(f'event type: {event.event_type}  path : {event.src_path}')
            self.daphne_process.kill()
            time.sleep(1)  # Add a delay here
            self.daphne_process = subprocess.Popen(['daphne', '-b', '0.0.0.0', '-p', '8000', 'anonchat.asgi:application'])

    def on_created(self, event):
        if '.git' not in event.src_path:
            print(f'event type: {event.event_type}  path : {event.src_path}')
            self.daphne_process.kill()
            time.sleep(1)  # And here
            self.daphne_process = subprocess.Popen(['daphne', '-b', '0.0.0.0', '-p', '8000', 'anonchat.asgi:application'])

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()