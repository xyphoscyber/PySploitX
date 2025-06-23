from rich.console import Console
from rich.table import Table
from core.module_manager import ModuleManager
from core.session_manager import SESSIONS
import shlex
import threading

class PySploitCLI:
    """
    The main command-line interface for PySploitX.
    """
    def __init__(self):
        self.console = Console()
        self.module_manager = ModuleManager()
        self.active_module = None
        self.prompt = "pysploitx > "
        self.background_jobs = {}
        self.job_id_counter = 1

    def print_banner(self):
        """
        Prints the PySploitX banner.
        """
        banner = """
[bold red]

 ######  #     # ####### ####### #       ####### ####### #     #
 #     #  #   #  #       #       #       #          #    #  #  #
 #     #   # #   #       #       #       #          #    #  #  #
 ######     #    #####   #####   #       #####      #    #  #  #
 #         # #   #       #       #       #          #    #  #  #
 #        #   #  #       #       #       #          #     ## ## 
 #       #     # ####### #       ####### #######    #      ###  

[/bold red]
        [bold blue]An Advanced Offensive Security Framework[/bold blue]
"""
        self.console.print(banner)
        self.console.print(f"[*] Loaded {len(self.module_manager.get_all_modules())} modules.")

    def run(self):
        """
        The main loop for the CLI.
        """
        self.print_banner()
        while True:
            try:
                user_input = self.console.input(self.prompt)
                if not user_input.strip():
                    continue
                
                parts = shlex.split(user_input)
                command = parts[0].lower()
                args = parts[1:]

                if command == 'exit':
                    for job_id in list(self.background_jobs.keys()):
                        self.kill_job(job_id)
                    break
                elif command == 'help':
                    self.show_help()
                elif command == 'list':
                    self.list_modules()
                elif command == 'load' or command == 'use':
                    if len(args) == 1: self.load_module(args[0])
                    else: self.console.print("[red]Usage: load <module_name>[/red]")
                elif command == 'info':
                    self.show_info(args)
                elif command == 'show':
                    if len(args) > 0 and args[0] == 'options': self.show_config()
                    else: self.console.print("[red]Usage: show options[/red]")
                elif command == 'config' or command == 'set':
                    if len(args) == 2: self.set_option(args[0], args[1])
                    else: self.console.print("[red]Usage: config <option> <value>[/red]")
                elif command == 'run' or command == 'exploit':
                    self.run_module()
                elif command == 'back':
                    self.unload_module()
                elif command == 'sessions':
                    self.handle_sessions(args)
                elif command == 'jobs':
                    self.list_jobs()
                elif command == 'kill':
                    if len(args) == 1: self.kill_job(int(args[0]))
                    else: self.console.print("[red]Usage: kill <job_id>[/red]")
                elif command == 'clear':
                    self.console.clear()
                else:
                    self.console.print(f"[red]Unknown command: {command}[/red]")

            except (EOFError, KeyboardInterrupt):
                self.console.print("\n[yellow]Exiting...[/yellow]")
                for job_id in list(self.background_jobs.keys()):
                    self.kill_job(job_id)
                break
            except Exception as e:
                self.console.print(f"[bold red]An error occurred: {e}[/bold red]")

    def show_help(self):
        """Displays the help message."""
        table = Table(title="Help - Core Commands")
        table.add_column("Command", style="cyan")
        table.add_column("Description")
        commands = {
            "list": "List all available modules.",
            "load <module>": "Load a module into the current context.",
            "info [module]": "Display information about the loaded module or a specific one.",
            "show options": "Show options for the currently loaded module.",
            "config <option> <value>": "Set a configuration option for the loaded module.",
            "run": "Execute the loaded module (runs handlers as background jobs).",
            "back": "Unload the current module.",
            "sessions -l": "List active sessions.",
            "sessions -i <id>": "Interact with an active session.",
            "sessions -k <id>": "Kill a specific session.",
            "jobs": "List background jobs (e.g., running handlers).",
            "kill <job_id>": "Stop a background job.",
            "clear": "Clear the console screen.",
            "exit": "Exit the framework.",
        }
        for cmd, desc in commands.items():
            table.add_row(cmd, desc)
        self.console.print(table)

    def list_modules(self):
        """Lists all available modules, categorized."""
        table = Table(title="Available Modules")
        table.add_column("Name", style="cyan")
        table.add_column("Description")
        modules = self.module_manager.get_all_modules()
        for name, module in sorted(modules.items()):
            table.add_row(name, module.get_info().get("Description", ""))
        self.console.print(table)

    def load_module(self, module_name):
        """Loads a module to be used."""
        module = self.module_manager.get_module(module_name)
        if module:
            self.active_module = module
            self.prompt = f"pysploitx [bold red]({module_name})[/bold red] > "
        else:
            self.console.print(f"[red]Module '{module_name}' not found.[/red]")

    def unload_module(self):
        """Unloads the currently active module."""
        self.active_module = None
        self.prompt = "pysploitx > "

    def show_info(self, args):
        """Shows information about a module."""
        module_to_show = self.module_manager.get_module(args[0]) if args else self.active_module
        if not module_to_show:
            self.console.print("[yellow]No module specified or loaded.[/yellow]")
            return
        info = module_to_show.get_info()
        self.console.print(f"\n[bold]Module Information: {info.get('Name')}[/bold]")
        self.console.print(f"  Description: {info.get('Description')}")
        self.show_config(module_to_show)

    def show_config(self, module=None):
        """Shows the configuration for the active module."""
        target_module = module or self.active_module
        if not target_module:
            self.console.print("[yellow]No module loaded.[/yellow]")
            return
        table = Table(title=f"Module Options: {target_module.get_info()['Name']}")
        table.add_column("Option", style="cyan")
        table.add_column("Current Value")
        table.add_column("Description")
        for option, (value, desc) in target_module.options.items():
            table.add_row(option, str(value), desc)
        self.console.print(table)

    def set_option(self, option, value):
        """Sets a configuration option for the active module."""
        if self.active_module and option.upper() in self.active_module.options:
            self.active_module.options[option.upper()][0] = value
            self.console.print(f"[green]{option.upper()} => {value}[/green]")
        else:
            self.console.print("[red]Option not found or no module loaded.[/red]")

    def run_module(self):
        """Executes the currently loaded module."""
        if not self.active_module:
            self.console.print("[yellow]No module loaded.[/yellow]")
            return

        module_name = self.active_module.get_info()['Name']
        if 'handler' in module_name:
            self.run_handler_module()
        else:
            self.run_exploit_module()

    def run_exploit_module(self):
        """Runs a standard exploit/recon/rat module in the foreground."""
        self.console.print(f"[*] Running module {self.active_module.get_info()['Name']}...")
        try:
            self.active_module.run(self.active_module.options)
        except Exception as e:
            self.console.print(f"[bold red]Module execution failed: {e}[/bold red]")

    def run_handler_module(self):
        """Runs a handler module in a background thread."""
        job_id = self.job_id_counter
        self.job_id_counter += 1
        thread = threading.Thread(target=self.active_module.run, args=(self.active_module.options,), daemon=True)
        thread.keep_running = True
        self.background_jobs[job_id] = (thread, self.active_module.get_info()['Name'])
        thread.start()
        self.console.print(f"[*] Handler module running as background job {job_id}.")

    def list_jobs(self):
        """Lists all running background jobs."""
        table = Table(title="Background Jobs")
        table.add_column("Job ID", style="cyan")
        table.add_column("Module Name")
        table.add_column("Status")
        if not self.background_jobs:
            self.console.print("[*] No background jobs running.")
            return
        for job_id, (thread, name) in self.background_jobs.items():
            status = "Running" if thread.is_alive() else "Stopped"
            table.add_row(str(job_id), name, status)
        self.console.print(table)

    def kill_job(self, job_id):
        """Stops a background job."""
        if job_id in self.background_jobs:
            thread, name = self.background_jobs.pop(job_id)
            thread.keep_running = False # Signal thread to stop
            self.console.print(f"[*] Stopped job {job_id} ({name}).")
        else:
            self.console.print("[red]Invalid job ID.[/red]")

    def handle_sessions(self, args):
        """Handles the 'sessions' command."""
        if not args or args[0] == '-l':
            SESSIONS.list_sessions()
        elif args[0] == '-i' and len(args) > 1:
            try:
                session_id = int(args[1])
                session = SESSIONS.get_session(session_id)
                if session and session.is_active:
                    session.shell(self.console)
                else:
                    self.console.print("[red]Invalid or inactive session ID.[/red]")
            except ValueError:
                self.console.print("[red]Session ID must be an integer.[/red]")
        elif args[0] == '-k' and len(args) > 1:
            try:
                session_id = int(args[1])
                SESSIONS.close_session(session_id)
            except ValueError:
                self.console.print("[red]Session ID must be an integer.[/red]")
        else:
            self.console.print("[red]Usage: sessions [-l | -i <id> | -k <id>][/red]")
