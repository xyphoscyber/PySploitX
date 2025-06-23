import requests
from core.base_module import BaseModule
from rich.console import Console

class SocialMediaFinder(BaseModule):
    """Checks for a username's existence on popular social media platforms."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'USERNAME': ['testuser', 'The username to search for.']
        }

    def run(self, options):
        """
        Executes the social media check.
        """
        username = options.get('USERNAME')
        console = Console()

        if not username:
            console.print("[!] USERNAME option not set.", style="bold red")
            return

        platforms = {
            'Instagram': f'https://www.instagram.com/{username}/',
            'Twitter': f'https://twitter.com/{username}',
            'GitHub': f'https://github.com/{username}',
            'Facebook': f'https://www.facebook.com/{username}',
            'Reddit': f'https://www.reddit.com/user/{username}',
            'Pinterest': f'https://www.pinterest.com/{username}/'
        }

        console.print(f"[*] Searching for username '{username}' across platforms...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        for platform, url in platforms.items():
            try:
                response = requests.get(url, headers=headers, timeout=7, allow_redirects=False)
                # Most platforms return 200 for existing profiles, some might redirect
                if response.status_code == 200:
                    console.print(f"[bold green][+] Found on {platform}:[/bold green] {url}")
                else:
                    console.print(f"[yellow][-] Not found on {platform} (Status: {response.status_code})[/yellow]")
            except requests.RequestException:
                console.print(f"[red][!] Error checking {platform}. Could be a connection issue or block.[/red]")

        console.print("\n[*] Scan complete.")
