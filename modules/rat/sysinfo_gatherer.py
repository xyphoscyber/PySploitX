import os
import platform
import socket
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class SysinfoGatherer(BaseModule):
    """Gathers basic system information from the local machine."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Collects and displays system information.
        """
        console = Console()
        console.print("[*] Gathering system information...")

        try:
            table = Table(title="System Information", show_header=True, header_style="bold magenta")
            table.add_column("Property", style="dim", width=20)
            table.add_column("Value")

            table.add_row("Operating System", platform.system())
            table.add_row("OS Release", platform.release())
            table.add_row("OS Version", platform.version())
            table.add_row("Architecture", platform.machine())
            table.add_row("Hostname", socket.gethostname())
            table.add_row("IP Address (local)", socket.gethostbyname(socket.gethostname()))
            table.add_row("User", os.getlogin())
            table.add_row("Processor", platform.processor())

            console.print(table)
            console.print("[bold green][+] System information gathered successfully.[/bold green]")

        except Exception as e:
            console.print(f"[!] Failed to gather system information: {e}", style="bold red")
