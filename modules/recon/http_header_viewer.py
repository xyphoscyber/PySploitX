import requests
from core.base_module import BaseModule
from rich.console import Console
from rich.table import Table

class HttpHeaderViewer(BaseModule):
    """Fetches and displays HTTP headers from a given URL."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'URL': ['http://example.com', 'The target URL to fetch headers from.']
        }

    def run(self, options):
        """
        Executes the HTTP header fetch.
        """
        url = options.get('URL')
        console = Console()

        if not url:
            console.print("[!] URL option not set.", style="bold red")
            return

        try:
            console.print(f"[*] Fetching headers for {url}...")
            # Allow redirects and verify SSL certificate by default
            response = requests.get(url, timeout=10, allow_redirects=True, verify=True)

            table = Table(title=f"HTTP Headers for {url}")
            table.add_column("Header", style="cyan")
            table.add_column("Value")

            for header, value in response.headers.items():
                table.add_row(header, value)
            
            console.print(table)
            console.print(f"\n[bold]Status Code:[/bold] {response.status_code} {response.reason}")

        except requests.exceptions.RequestException as e:
            console.print(f"[!] An error occurred while requesting the URL: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
