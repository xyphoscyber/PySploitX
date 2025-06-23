#!/usr/bin/env python3

from core.cli import PySploitCLI

def main():
    """
    Main function to start the PySploitX framework.
    """
    try:
        cli = PySploitCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n[!] User interrupt. Exiting PySploitX.")
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
