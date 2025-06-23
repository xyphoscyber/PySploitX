import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from core.base_module import BaseModule
from rich.console import Console

class WebsiteCloner(BaseModule):
    """Clones a website to a local directory."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'URL': ['http://example.com', 'The URL of the website to clone.'],
            'OUTPUT_DIR': ['cloned_site', 'The directory to save the cloned site.']
        }

    def run(self, options):
        """
        Executes the website cloning process.
        """
        url = options.get('URL')
        output_dir = options.get('OUTPUT_DIR')
        console = Console()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        try:
            console.print(f"[*] Cloning website: {url}")
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            parsed_url = urlparse(url)

            # Save the main HTML file
            filename = os.path.join(output_dir, os.path.basename(parsed_url.path) or 'index.html')
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            console.print(f"[+] Saved HTML to {filename}")

            # Find and download CSS, JS, and images
            for tag in soup.find_all(['link', 'script', 'img']):
                attr = ''
                if tag.name == 'link' and 'href' in tag.attrs:
                    attr = 'href'
                elif tag.name == 'script' and 'src' in tag.attrs:
                    attr = 'src'
                elif tag.name == 'img' and 'src' in tag.attrs:
                    attr = 'src'
                
                if attr:
                    asset_url = urljoin(url, tag[attr])
                    self._download_asset(asset_url, output_dir, console)

            console.print(f"[bold green][+] Website cloned successfully to {output_dir}[/bold green]")

        except requests.RequestException as e:
            console.print(f"[!] Error fetching URL: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An error occurred: {e}", style="bold red")

    def _download_asset(self, asset_url, output_dir, console):
        try:
            response = requests.get(asset_url, stream=True)
            response.raise_for_status()

            parsed_url = urlparse(asset_url)
            # Create subdirectories if they exist in the URL path
            path_parts = parsed_url.path.strip('/').split('/')
            asset_dir = os.path.join(output_dir, *path_parts[:-1])
            if not os.path.exists(asset_dir):
                os.makedirs(asset_dir)

            asset_filename = os.path.join(asset_dir, path_parts[-1])
            with open(asset_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            console.print(f"[+] Downloaded asset: {asset_filename}")
        except requests.RequestException as e:
            console.print(f"[!] Failed to download {asset_url}: {e}", style="yellow")
