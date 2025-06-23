import os
import shutil
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class FileManager(BaseModule):
    """Provides basic file system operations on the target."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'COMMAND': ['ls .', 'The command to run (ls, cat, rm). E.g., ls /tmp, cat /etc/passwd, rm /tmp/file.txt'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the file management command.
        """
        command_str = options.get('COMMAND')
        console = Console()

        parts = command_str.split(' ', 1)
        operation = parts[0].lower()
        path = parts[1] if len(parts) > 1 else '.'

        console.print(f"[*] Executing file manager command: {operation} on path: {path}")

        try:
            if operation == 'ls':
                self._list_directory(path, console)
            elif operation == 'cat':
                self._read_file(path, console)
            elif operation == 'rm':
                self._delete_file(path, console)
            else:
                console.print(f"[!] Invalid operation: {operation}. Use 'ls', 'cat', or 'rm'.", style="bold red")

        except FileNotFoundError:
            console.print(f"[!] Path not found: {path}", style="bold red")
        except PermissionError:
            console.print(f"[!] Permission denied for path: {path}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")

    def _list_directory(self, path, console):
        """Lists the contents of a directory."""
        if not os.path.isdir(path):
            console.print(f"[!] Not a directory: {path}", style="bold red")
            return

        table = Table(title=f"Contents of {path}", show_header=True, header_style="bold magenta")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="yellow")
        table.add_column("Size (Bytes)", justify="right")

        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isdir(item_path):
                    table.add_row(item, "Directory", "-")
                else:
                    size = os.path.getsize(item_path)
                    table.add_row(item, "File", str(size))
            except (FileNotFoundError, PermissionError):
                table.add_row(item, "N/A", "N/A")
        
        console.print(table)

    def _read_file(self, path, console):
        """Reads and prints the contents of a file."""
        if not os.path.isfile(path):
            console.print(f"[!] Not a file: {path}", style="bold red")
            return
        
        with open(path, 'r', errors='ignore') as f:
            content = f.read()
        
        console.print(f"--- Contents of {path} ---")
        console.print(content)
        console.print("---------------------------")

    def _delete_file(self, path, console):
        """Deletes a file."""
        if not os.path.isfile(path):
            console.print(f"[!] Not a file: {path}", style="bold red")
            return
        
        os.remove(path)
        console.print(f"[bold green][+] File deleted successfully: {path}[/bold green]")
