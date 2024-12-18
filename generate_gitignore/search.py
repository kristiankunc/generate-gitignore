# -*- coding: utf-8 -*-

import sys, os
from colorama import Fore, Style
msvcrt = __import__('msvcrt') if os.name == 'nt' else None
tty = __import__('tty') if os.name != 'nt' else None
termios = __import__('termios') if os.name != 'nt' else None

def handle_search(prompt: str, options: list[str]) -> int:
    os.system('cls' if os.name == 'nt' else 'clear')
        
    search_term = ""
    cursor_pos = 0

    def refresh_display():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{prompt}\n{Fore.WHITE}Interactive search (press Enter to select, Ctrl+C to cancel):")
        
        if not search_term:
            print("\nAll templates:")
            displayed = options[:10]
        else:
            matches = [name for name in options if search_term.lower() in name.lower()]
            displayed = matches[:10]
            
        for i, name in enumerate(displayed):
            if cursor_pos == i:
                print(f"{Fore.GREEN}> {name}{Style.RESET_ALL}")
            else:
                print(f"  {Fore.BLUE}{name}{Style.RESET_ALL}")
                
        if len(displayed) > 10:
            print(f"\n{Fore.YELLOW}...and {len(options) - 10} more{Style.RESET_ALL}")
            
        print(f"\nSearch: {search_term}", end='', flush=True)

    while True:
        refresh_display()
        
        if os.name == 'posix':
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x03':  # Ctrl+C
                    print(f"\n{Fore.RED}✘ Aborting...{Style.RESET_ALL}")
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
                if ch == '\x03':  # Ctrl+C
                    print(f"\n{Fore.RED}✘ Aborting...{Style.RESET_ALL}")
                    sys.exit(0)

        matches = [name for name in options if search_term.lower() in name.lower()]
                    
        if ch == '\r':  # Enter key
            if matches:
                selected_name = matches[cursor_pos]
                return options.index(selected_name)
            
        elif ch == '\x1b[A':  # Up arrow
            cursor_pos = max(0, cursor_pos - 1)

        elif ch == '\x1b[B':  # Down arrow
            cursor_pos = min(len(matches[:10]) - 1, cursor_pos + 1)

        elif ch in ('\x7f', '\b'):  # Backspace
            search_term = search_term[:-1]
            if cursor_pos >= len(matches[:10]):
                cursor_pos = 0

        elif len(ch) == 1:  # Regular character
            search_term += ch
            if cursor_pos >= len(matches[:10]):
                cursor_pos = 0
