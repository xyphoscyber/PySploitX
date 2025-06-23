# PySploitX - Advanced Offensive Security Framework

PySploitX is a modular and extensible offensive security framework written in Python, inspired by Metasploit. It is designed for penetration testers and security researchers to streamline the process of reconnaissance, exploitation, and post-exploitation with a powerful, interactive CLI.

## 🚀 Features

-   **Interactive CLI:** A powerful and user-friendly command-line interface similar to `msfconsole`.
-   **Modular Architecture:** Easily add new modules for exploits, reconnaissance, RATs, and handlers.
-   **Session Management:** Full-featured session handling for reverse shells. Interact with, list, and kill sessions on the fly.
-   **Background Jobs:** Run listeners and other long-running tasks as background jobs without blocking the CLI.
-   **Real-World Modules:** Includes a growing collection of modules for reconnaissance, vulnerability scanning, and exploitation.
-   **Dynamic Configuration:** Configure module options on the fly.
-   **Cross-Platform:** Core framework runs on both Windows and Linux.

## 📂 Folder Structure

```
PySploitX/
├── core/                   # Core framework components
│   ├── cli.py              # Command-Line Interface
│   ├── module_manager.py   # Module loading and management
│   ├── session_manager.py  # Session creation and interaction
│   └── base_module.py      # Base class for all modules
├── modules/                # All modules
│   ├── exploits/           # Exploit modules
│   ├── handlers/           # Listener modules (e.g., reverse TCP)
│   ├── recon/              # Reconnaissance modules
│   └── rat/                # Remote Access Trojan modules
├── pysploitx.py            # Main entry point
├── requirements.txt        # Python dependencies
└── README.md
```

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/pysploitx.git
    cd pysploitx
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 📖 Usage

### Launching the Framework

```bash
python pysploitx.py
```

### Basic Commands

-   `list`: List all available modules.
-   `load <module>`: Load a module (e.g., `load exploits/unrealircd_backdoor`).
-   `show options`: Display options for the loaded module.
-   `config <option> <value>`: Set a module option (e.g., `config RHOST 127.0.0.1`).
-   `run`: Execute the loaded module.
-   `back`: Unload the current module.

### Session & Job Management Example

1.  **Start a listener**:
    ```
    pysploitx > load handlers/reverse_tcp_handler
    pysploitx (handlers/reverse_tcp_handler) > run
    [*] Handler module running as background job 1.
    ```

2.  **List background jobs**:
    ```
    pysploitx > jobs
    ```

3.  **After a payload connects, list sessions**:
    ```
    pysploitx > sessions -l
    ```

4.  **Interact with a session**:
    ```
    pysploitx > sessions -i 1
    [*] Interacting with session 1...
    $ whoami
    root
    $ exit
    ```

5.  **Kill a job or session**:
    ```
    pysploitx > kill 1
    pysploitx > sessions -k 1
    ```

## 📝 Project Status & Roadmap

- [x] Interactive CLI with core commands.
- [x] Modular architecture for exploits, recon, and RATs.
- [x] **Session management for reverse shells.**
- [x] **Background job system for handlers.**
- [ ] Payload generation (e.g., standalone reverse shell executables).
- [ ] Advanced post-exploitation modules (e.g., privilege escalation, lateral movement).
- [ ] Database integration for storing loot and host information.
- [ ] Evasion and obfuscation techniques.
