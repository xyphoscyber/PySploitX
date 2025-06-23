import hashlib
from core.base_module import BaseModule
from rich.console import Console

class HashCracker(BaseModule):
    """Attempts to crack a hash using a simple dictionary attack."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'HASH': ['', 'The hash to crack.'],
            'HASH_TYPE': ['md5', 'The type of hash (md5, sha1, sha256).'],
            'WORDLIST': ['', 'Path to a wordlist file (optional, uses a small built-in list if empty).']
        }

    def run(self, options):
        """
        Executes the hash cracking process.
        """
        target_hash = options.get('HASH')
        hash_type = options.get('HASH_TYPE').lower()
        wordlist_path = options.get('WORDLIST')
        console = Console()

        if not target_hash:
            console.print("[!] HASH option not set.", style="bold red")
            return

        if hash_type not in ['md5', 'sha1', 'sha256']:
            console.print("[!] Invalid HASH_TYPE. Use 'md5', 'sha1', or 'sha256'.", style="bold red")
            return

        hash_func = getattr(hashlib, hash_type)

        if wordlist_path:
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    wordlist = [line.strip() for line in f]
                console.print(f"[*] Loaded {len(wordlist)} words from {wordlist_path}.")
            except FileNotFoundError:
                console.print(f"[!] Wordlist file not found: {wordlist_path}", style="bold red")
                return
        else:
            console.print("[*] No wordlist provided. Using a small, built-in list.")
            wordlist = ['password', '123456', '123456789', 'qwerty', 'admin', 'root', '12345', 'test']

        console.print(f"[*] Starting {hash_type} hash crack for: {target_hash}")
        found = False
        for word in wordlist:
            hashed_word = hash_func(word.encode()).hexdigest()
            if hashed_word == target_hash:
                console.print(f"[bold green][+] Hash cracked! The password is: {word}[/bold green]")
                found = True
                break
        
        if not found:
            console.print("[yellow][-] Hash not found in the provided wordlist.[/yellow]")
