import argparse
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from . import alpss_main

"""
Credit to Michael Cho
https://michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-directory
"""


class Watcher:
    # this is the directory where you will add the files to
    DIRECTORY_TO_WATCH = os.getcwd() + "/input_data"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            print("Error in Watcher.run: ", e)

        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == "created":
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

            fname = os.path.split(event.src_path)[1]
            print(f"File Created:  {fname}")

            # use these function inputs the same as for the non-automated function alpss_run.py
            alpss_main(filename=fname)


def start_watcher():
    w = Watcher()
    w.run()


def run_alpss():
    parser = argparse.ArgumentParser(description="Run ALPSS on a file")
    parser.add_argument(
        "filename",
        type=str,
        help="The name of the file to run ALPSS on",
    )
    args = parser.parse_args()
    alpss_main(filename=args.filename)
