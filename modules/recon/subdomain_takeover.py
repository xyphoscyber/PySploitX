import requests
import socket
import threading
from queue import Queue
from core.base_module import BaseModule
from rich.console import Console

class SubdomainTakeover(BaseModule):
    """Scans for subdomains vulnerable to takeover."""

    def get_options(self):
        """Returns the options for this module."""
        return {
            'DOMAIN': ['', 'The target domain (e.g., example.com).'],
            'WORDLIST': ['/usr/share/wordlists/dns/subdomains-top1000-5000.txt', 'Path to the subdomain wordlist.'],
            'THREADS': [20, 'Number of threads to use.']
        }

    TAKEOVER_FINGERPRINTS = [
        "There isn't a GitHub Pages site here.", "NoSuchBucket", "The specified bucket does not exist",
        "Sorry, this page is no longer available.", "The page you were looking for doesn't exist.",
        "This domain is for sale", "Fastly error: unknown domain"
    ]

    def _worker(self, q, domain, console):
        """Worker thread function."""
        while not q.empty():
            subdomain = q.get()
            full_domain = f"{subdomain}.{domain}"
            try:
                # Check CNAME
                socket.gethostbyname(full_domain)
                # Check HTTP content for fingerprints
                for scheme in ['http://', 'https://']:
                    try:
                        r = requests.get(f"{scheme}{full_domain}", timeout=5, verify=False)
                        for fingerprint in self.TAKEOVER_FINGERPRINTS:
                            if fingerprint in r.text:
                                console.print(f"[bold red][+] Potential Takeover Found: {full_domain}[/bold red] (Fingerprint: '{fingerprint}')")
                                break
                    except requests.RequestException:
                        continue
            except socket.gaierror:
                pass # Subdomain doesn't resolve
            finally:
                q.task_done()

    def run(self, options):
        """Executes the subdomain takeover scan."""
        domain = options.get('DOMAIN')
        wordlist_path = options.get('WORDLIST')
        num_threads = int(options.get('THREADS'))
        console = Console()

        if not domain or not wordlist_path:
            console.print("[!] DOMAIN and WORDLIST must be set.", style="bold red")
            return

        try:
            with open(wordlist_path, 'r') as f:
                wordlist = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            console.print(f"[!] Wordlist not found at: {wordlist_path}", style="bold red")
            return

        console.print(f"[*] Scanning {len(wordlist)} subdomains for potential takeover on '{domain}'...")
        q = Queue()
        for word in wordlist:
            q.put(word)

        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker, args=(q, domain, console))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        q.join()
        console.print("[*] Subdomain takeover scan complete.")