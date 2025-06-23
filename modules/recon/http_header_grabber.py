import requests
from core.base_module import BaseModule
from rich.console import Console
from rich.panel import Panel

class HttpHeaderGrabber(BaseModule):
    """Fetches and displays HTTP headers from a web server."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'URL': ['', 'The target URL (e.g., http://example.com).']
        }

    def run(self, options):
        """
        Executes the HTTP header grabber.
        """
        url = options.get('URL')
        console = Console()

        if not url:
            console.print("[!] URL must be set.", style="bold red")
            return

        console.print(f"[*] Fetching HTTP headers from {url}...")
        headers = {'User-Agent': 'PySploitX Header Grabber'}

        try:
            response = requests.head(url, headers=headers, timeout=15, verify=False, allow_redirects=True)
            
            header_text = f"[bold]Status Code:[/bold] {response.status_code} {response.reason}\\n"
            for key, value in response.headers.items():
                header_text += f"[bold cyan]{key}:[/bold cyan] {value}\\n"

            console.print(Panel(
                header_text.strip(),
                title=f"[bold]HTTP Headers for {response.url}[/bold]",
                expand=False
            ))

        except requests.RequestException as e:
            console.print(f"[!] Request failed: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")