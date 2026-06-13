#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading
import time
import subprocess
import urllib.request
import json
from urllib.error import URLError

def init_ngrok():
    """Starts ngrok and prints the public URL."""
    try:
        # Check if ngrok is already running
        try:
            with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels") as response:
               pass # Already running
        except URLError:
            # Not running, start it
            print("🚀 Starting ngrok tunnel...")
            subprocess.Popen(
                ["ngrok", "http", "8000"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(2) # Wait for startup

        # Get and print the URL
        try:
            req = urllib.request.Request("http://127.0.0.1:4040/api/tunnels")
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                tunnels = data.get('tunnels', [])
                for tunnel in tunnels:
                    public_url = tunnel.get('public_url')
                    if public_url:
                        print(f"\n🌍 \033[92mNgrok Public URL is usable: {public_url}\033[0m\n")
                        return
        except Exception as e:
            print(f"⚠️  Could not retrieve ngrok URL: {e}")

    except Exception as e:
        print(f"⚠️  Could not init ngrok: {e}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    # Auto-start ngrok only for runserver and in the main process (not the reloader)
    if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') != 'true':
        threading.Thread(target=init_ngrok, daemon=True).start()

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()