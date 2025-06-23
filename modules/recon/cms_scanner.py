import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from core.base_module import BaseModule
from rich.console import Console

class CmsScanner(BaseModule):
    """Identifies the Content Management System (CMS) of a website."""

    def get_options(self):
        """Returns the options for this module."""
        return {
            'URL': ['', 'The base URL of the target website (e.g., http://example.com).']
        }

    CMS_FINGERPRINTS = {
        'WordPress': [
            ('file', '/wp-login.php'),
            ('file', '/wp-admin/'),
            ('meta', 'WordPress'),
            ('string', '/wp-content/'),
            ('string', '/wp-includes/')
        ],
        'Joomla': [
            ('file', '/administrator/'),
            ('meta', 'Joomla!'),
            ('string', 'com_content')
        ],
        'Drupal': [
            ('file', '/user/login'),
            ('meta', 'Drupal'),
            ('string', '/sites/default/files/'),
            ('string', 'Drupal.settings')
        ],
        'Magento': [
            ('file', '/downloader/'),
            ('string', 'skin/frontend/'),
            ('string', 'Magento')
        ],
        'Shopify': [
            ('string', 'cdn.shopify.com'),
            ('string', 'Shopify.theme')
        ],
        'vBulletin': [
            ('meta', 'vBulletin'),
            ('string', 'vb_')
        ]
    }

    def run(self, options):
        """Executes the CMS scan."""
        url = options.get('URL')
        console = Console()

        if not url:
            console.print("[!] URL must be set.", style="bold red")
            return

        console.print(f"[*] Scanning {url} for CMS signatures...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

        try:
            response = requests.get(url, headers=headers, timeout=15, verify=False, allow_redirects=True)
            response.raise_for_status()
            content = response.text
            soup = BeautifulSoup(content, 'lxml')

            for cms, fingerprints in self.CMS_FINGERPRINTS.items():
                for f_type, f_value in fingerprints:
                    if f_type == 'file':
                        test_url = urljoin(url, f_value)
                        try:
                            file_res = requests.head(test_url, headers=headers, timeout=5, verify=False, allow_redirects=True)
                            if file_res.status_code == 200:
                                console.print(f"[bold green][+] Found CMS: {cms}[/bold green] (Reason: Found file/path at {test_url})")
                                return
                        except requests.RequestException:
                            continue
                    elif f_type == 'meta':
                        meta_tag = soup.find('meta', attrs={'name': ['generator', 'Generator']})
                        if meta_tag and meta_tag.get('content') and f_value in meta_tag.get('content', ''):
                            console.print(f"[bold green][+] Found CMS: {cms}[/bold green] (Reason: Found meta tag: {meta_tag.get('content')})")
                            return
                    elif f_type == 'string':
                        if f_value in content:
                            console.print(f"[bold green][+] Found CMS: {cms}[/bold green] (Reason: Found string '{f_value}' in page source)")
                            return
            
            console.print("[*] No definitive CMS identified based on fingerprints.")

        except requests.RequestException as e:
            console.print(f"[!] Request failed: {e}", style="bold red")
        except Exception as e:
            console.print(f"[!] An unexpected error occurred: {e}", style="bold red")
