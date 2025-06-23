import requests
from bs4 import BeautifulSoup
from core.base_module import BaseModule
from rich.console import Console

class CmsDetector(BaseModule):
    """Identifies the Content Management System (CMS) of a website."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'URL': ['http://example.com', 'The target URL to check for a CMS.']
        }

    def run(self, options):
        """
        Executes the CMS detection.
        """
        url = options.get('URL')
        console = Console()

        if not url:
            console.print("[!] URL option not set.", style="bold red")
            return

        # Signatures for different CMS
        cms_signatures = {
            'WordPress': [
                '/wp-content/', '/wp-includes/',
                {'tag': 'meta', 'attrs': {'name': 'generator', 'content': 'WordPress'}}
            ],
            'Joomla': [
                '/media/com_joomla/', 'index.php?option=com_users',
                {'tag': 'meta', 'attrs': {'name': 'generator', 'content': 'Joomla!'}}
            ],
            'Drupal': [
                '/sites/all/', '/sites/default/',
                {'tag': 'meta', 'attrs': {'name': 'Generator', 'content': 'Drupal'}}
            ],
            'Shopify': [
                'cdn.shopify.com',
                {'tag': 'script', 'attrs': {'src': 'cdn.shopify.com'}}
            ],
            'Magento': [
                '/skin/frontend/', 'Mage.Cookies',
                {'tag': 'script', 'attrs': {'type': 'text/javascript', 'src': 'js/mage/'}}
            ]
        }

        try:
            console.print(f"[*] Checking CMS for {url}...")
            response = requests.get(url, timeout=10, headers={'User-Agent': 'PySploitX-CMS-Detector'})
            content = response.text
            soup = BeautifulSoup(content, 'lxml')

            detected_cms = None
            for cms, signatures in cms_signatures.items():
                for sig in signatures:
                    if isinstance(sig, str) and sig in content:
                        detected_cms = cms
                        break
                    elif isinstance(sig, dict):
                        if soup.find(sig['tag'], sig['attrs']):
                            detected_cms = cms
                            break
                if detected_cms:
                    break
            
            if detected_cms:
                console.print(f"[bold green][+] Detected CMS: {detected_cms}[/bold green]")
            else:
                console.print("[yellow]Could not identify the CMS.[/yellow]")

        except requests.exceptions.RequestException as e:
            console.print(f"[!] Could not connect to {url}: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
