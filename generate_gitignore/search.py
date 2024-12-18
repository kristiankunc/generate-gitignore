# -*- coding: utf-8 -*-

import sys, os
from colorama import Fore, Style
msvcrt = __import__('msvcrt') if os.name == 'nt' else None
tty = __import__('tty') if os.name != 'nt' else None
termios = __import__('termios') if os.name != 'nt' else None

def handle_search(templates: dict) -> str:
    os.system('cls' if os.name == 'nt' else 'clear')
        
    template_names = [template["name"] for template in templates]
    search_term = ""
    cursor_pos = 0

    def refresh_display():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.WHITE}Interactive search (press Enter to select, Ctrl+C to exit):")
        
        if not search_term:
            print("\nAll templates:")
            displayed = template_names[:10]
        else:
            matches = [name for name in template_names if search_term.lower() in name.lower()]
            displayed = matches[:10]
            
        for i, name in enumerate(displayed):
            if cursor_pos == i:
                print(f"{Fore.GREEN}> {name}{Style.RESET_ALL}")
            else:
                print(f"  {Fore.BLUE}{name}{Style.RESET_ALL}")
                
        if len(displayed) > 10:
            print(f"\n{Fore.YELLOW}...and {len(template_names) - 10} more{Style.RESET_ALL}")
            
        print(f"\nSearch: {search_term}", end="")

    while True:
        refresh_display()
        
        if os.name == 'posix':
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x03':  # Ctrl+C on POSIX
                    print(f"\n{Fore.RED}Aborting...{Style.RESET_ALL}")
                    sys.exit(0)

                if ch == '\x1b':  # Escape sequence
                    ch += sys.stdin.read(2)

            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        else:
            ch = msvcrt.getch()
            if ch == b'\xe0':  # Special key prefix
                ch = msvcrt.getch()

                if ch == b'H':  # Up arrow
                    ch = '\x1b[A'

                elif ch == b'P':  # Down arrow
                    ch = '\x1b[B'

            else:
                ch = ch.decode('utf-8', errors='ignore')
                if ch == '\x03':  # Ctrl+C on Windows
                    print(f"\n{Fore.RED}Aborting...{Style.RESET_ALL}")
                    sys.exit(0)

        if ch == '\r':  # Enter key
            matches = [name for name in template_names if search_term.lower() in name.lower()]
            if matches:
                print("\n")
                return matches[cursor_pos]
            else:
                print(f"\n{Fore.RED}No matches found{Style.RESET_ALL}")
                input("Press Enter to continue...")
            search_term = ""
            cursor_pos = 0
            
        elif ch == '\x1b[A':  # Up arrow
            cursor_pos = max(0, cursor_pos - 1)

        elif ch == '\x1b[B':  # Down arrow
            matches = [name for name in template_names if search_term.lower() in name.lower()]
            cursor_pos = min(len(matches[:10]) - 1, cursor_pos + 1)

        elif ch in ('\x7f', '\b'):  # Backspace key
            search_term = search_term[:-1]
            matches = [name for name in template_names if search_term.lower() in name.lower()]
            if cursor_pos >= len(matches[:10]):
                cursor_pos = 0

        elif len(ch) == 1:  # Regular character
            search_term += ch
            matches = [name for name in template_names if search_term.lower() in name.lower()]
            if cursor_pos >= len(matches[:10]):
                cursor_pos = 0
