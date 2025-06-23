import requests
import os
from core.base_module import BaseModule
from rich.console import Console

class FileDownloader(BaseModule):
    """Downloads a file from a URL to the target machine."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'URL': ['', 'The URL of the file to download.'],
            'DEST_PATH': ['', 'The destination path to save the file (e.g., C:\\Users\\Public\\file.exe or /tmp/file).']
        }

    def run(self, options):
        """
        Executes the file download process.
        """
        url = options.get('URL')
        dest_path = options.get('DEST_PATH')
        console = Console()

        if not url or not dest_path:
            console.print("[!] URL and DEST_PATH must be set.", style="bold red")
            return

        console.print(f"[*] Downloading file from {url} to {dest_path}...")

        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Ensure the destination directory exists
            dest_dir = os.path.dirname(dest_path)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            with open(dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            console.print(f"[bold green][+] File downloaded successfully to {dest_path}[/bold green]")

        except requests.exceptions.RequestException as e:
            console.print(f"[!] Failed to download file: {e}", style="bold red")
        except OSError as e:
            console.print(f"[!] Failed to save file to {dest_path}: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
