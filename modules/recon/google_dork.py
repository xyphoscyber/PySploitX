from googlesearch import search
from core.base_module import BaseModule
from rich.console import Console

class GoogleDork(BaseModule):
    """Performs Google dorking to find indexed information."""

    def get_options(self):
        """
        Returns the options for this module.
        """
        return {
            'QUERY': ['site:example.com filetype:pdf', 'The Google dork query to execute.'],
            'NUM_RESULTS': ['10', 'The number of results to retrieve.']
        }

    def run(self, options):
        """
        Executes the Google dork query.
        """
        query = options.get('QUERY')
        num_results_str = options.get('NUM_RESULTS')
        console = Console()

        if not query:
            console.print("[!] QUERY option not set.", style="bold red")
            return

        try:
            num_results = int(num_results_str)
        except ValueError:
            console.print("[!] Invalid number for NUM_RESULTS. Must be an integer.", style="bold red")
            return

        try:
            console.print(f"[*] Executing Google dork query: '{query}'")
            results = search(query, num_results=num_results)
            
            if results:
                console.print(f"\n[bold green]Found {len(results)} results:[/bold green]")
                for i, result in enumerate(results, 1):
                    console.print(f"  {i}. {result}")
            else:
                console.print("[yellow]No results found for the query.[/yellow]")

        except Exception as e:
            console.print(f"[!] An error occurred during the search: {e}", style="bold red")
            console.print("[!] Note: Frequent use may lead to temporary IP blocks from Google.", style="yellow")
