import pyperclip
import time
from core.base_module import BaseModule
from rich.console import Console

class ClipboardLogger(BaseModule):
    """Monitors and logs clipboard content."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'DURATION': [60, 'The duration in seconds to monitor the clipboard.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the clipboard logger.
        """
        duration = int(options.get('DURATION'))
        console = Console()

        console.print(f"[*] Starting clipboard logger for {duration} seconds...")
        console.print("[yellow]Press Ctrl+C to stop early.[/yellow]")

        recent_value = ""
        start_time = time.time()

        try:
            while time.time() - start_time < duration:
                clipboard_content = pyperclip.paste()
                if clipboard_content != recent_value:
                    recent_value = clipboard_content
                    if recent_value.strip():
                        console.print(f"[bold green][+] Clipboard changed:[/bold green] {recent_value}")
                time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\\n[*] Logger stopped by user.")
        except pyperclip.PyperclipException as e:
            console.print(f"[!] Clipboard functionality is not available on this system: {e}", style="bold red")
            console.print("[!] You may need to install a backend (e.g., `sudo apt-get install xclip` on Debian/Ubuntu).")
        
        console.print("[*] Clipboard logger finished.")