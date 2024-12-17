#!/usr/bin/python
# -*- coding: utf-8 -*-

import tty, termios, sys, os, requests, argparse
from difflib import get_close_matches
from typing import Optional, List
from .cache import load_from_cache, save_to_cache
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def main():
    parser = construct_parser()
    args = parser.parse_args()
    
    if args.command == "list":
        templates = load_templates()
        
        for template in templates:
            print(f"{Fore.WHITE}{template['name']}{Style.RESET_ALL}")

        sys.exit(0)

    if args.command == "search":
        templates = load_templates()
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
                
            for name in displayed:
                if cursor_pos == displayed.index(name):
                    print(f"{Fore.GREEN}> {name}{Style.RESET_ALL}")
                else:
                    print(f"  {Fore.BLUE}{name}{Style.RESET_ALL}")
                    
            if len(displayed) > 10:
                print(f"\n{Fore.YELLOW}...and {len(template_names) - 10} more{Style.RESET_ALL}")
                
            print(f"\nSearch: {search_term}", end="")

        while True:
            refresh_display()
            
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            if ch == '\r':  # Enter key
                matches = [name for name in template_names if search_term.lower() in name.lower()]
                if matches:
                    args.template = matches[cursor_pos]
                    args.command = "use"
                    break
                else:
                    print(f"\n{Fore.RED}No matches found{Style.RESET_ALL}")
                    input("Press Enter to continue...")

            elif ch in ('\x7f', '\x08'):  # Backspace
                search_term = search_term[:-1]
                cursor_pos = 0
                
            elif ch == '\x1b':  # Escape sequence
                next_ch = sys.stdin.read(2)
                if next_ch == '[A':  # Up arrow
                    cursor_pos = max(0, cursor_pos - 1)
                elif next_ch == '[B':  # Down arrow
                    matches = [name for name in template_names if search_term.lower() in name.lower()]
                    cursor_pos = min(len(matches[:10]) - 1, cursor_pos + 1)
            elif ch.isprintable():
                search_term += ch
                cursor_pos = 0


    if args.command == "use":
        templates = load_templates()

        template = next((template for template in templates if template["name"].lower() == args.template.lower()), None)
        if template:
            print(f"{Fore.GREEN}Applying {template['name']}...{Style.RESET_ALL}")

            if (os.path.exists(".gitignore") and os.path.getsize(".gitignore") > 0):
                overwrite = get_bool_answer(f"{Fore.YELLOW}A .gitignore file already exists. Overwrite it?{Style.RESET_ALL}")
                if not overwrite:
                    print(f"{Fore.RED}✘ Aborting...{Style.RESET_ALL}")
                    sys.exit(0)
            
            with open(".gitignore", "w") as f:
                template_content = fetch_template(template["download_url"])
                if template_content is None or template_content == "":
                    print(f"{Fore.RED}✘ Error fetching template{Style.RESET_ALL}")
                    sys.exit(1)

                f.write(template_content)

            print(f"{Fore.GREEN}.gitignore file created successfully{Style.RESET_ALL}")
            
        else:
            print(f"{Fore.RED}Template '{args.use}' not found{Style.RESET_ALL}")
        
        sys.exit(0)

    parser.print_help()
    


def fetch_templates(url: str) -> dict:
    """
    Fetch the list of available .gitignore templates from the specified template URL.

    :param url: The URL of the JSON file containing the template data.
    :return: A dictionary containing the template data.
    """
    
    response = requests.get(url)

    if response.ok:
        return response.json()
    else:
        print(f"{Fore.RED}✘ Error fetching templates: {response.status_code}{Style.RESET_ALL}")
        return {}

def fetch_template(url: str) -> Optional[str]:
    """
    Fetch the content of a .gitignore template from the specified URL.

    :param url: The URL of the .gitignore template.
    :return: The content of the .gitignore template.
    """
    response = requests.get(url)

    if response.ok:
        return response.text
    else:
        print(f"{Fore.RED}✘ Error fetching template: {response.status_code}{Style.RESET_ALL}")
        return None
    
    
def construct_parser() -> argparse.ArgumentParser:
    """
    Construct an argument parser with subcommands for each .gitignore template.

    :param templates: A dictionary containing the template data.
    :return: An argument parser with subcommands for each template.
    """
    parser = argparse.ArgumentParser(description="Generate .gitignore files for your projects")

    subparsers = parser.add_subparsers(dest='command')
    
    list_parser = subparsers.add_parser('list', help='List available .gitignore templates')
    
    search_parser = subparsers.add_parser('search', help='Search for a specific .gitignore template')
    
    use_parser = subparsers.add_parser('use', help='Use a specific .gitignore template')
    use_parser.add_argument('template', help='Template name to use')


    return parser

def find_closest_match(query: str, candidates: List[str], cutoff: float = 0.6) -> List[str]:
    """
    Find the closest matches to a query in a list of strings.

    :param query: The query string to search for.
    :param candidates: A list of candidate strings to search within.
    :param cutoff: The similarity threshold (0 to 1). Only matches with a score >= cutoff are considered.
    :return: A list of matching strings, ordered by similarity.
    """
    matches = get_close_matches(query, candidates, n=3, cutoff=cutoff)
    return matches
    
def get_bool_answer(prompt: str) -> bool:
    """
    Prompt the user for a yes/no answer and return the result as a boolean.
    Pressing Enter defaults to yes.

    :param prompt: The prompt to display to the user.
    :return: True if the user answers 'yes' or presses Enter, False if the user answers 'no'.
    """

    answer = input(f"{prompt} (Y/n): ").lower()
    if answer in ["y", "yes", ""]: 
        return True
    elif answer in ["n", "no"]:
        return False
    else:
        print(f"{Fore.RED}Invalid input. Please enter 'y', 'n', or press Enter.{Style.RESET_ALL}")
        return get_bool_answer(prompt)

def load_templates() -> dict:
    templates = load_from_cache("templates.txt")
    if not templates or templates == {} or templates == []:
        templates = fetch_templates("https://raw.githubusercontent.com/kristiankunc/generate-gitignore/refs/heads/main/templates.json")
        save_to_cache(templates, "templates.txt")

        print(f"{Fore.GREEN}✔ Templates successfully loaded from remote{Style.RESET_ALL}")
    
    else:
        print(f"{Fore.GREEN}✔ Templates successfully loaded from cache{Style.RESET_ALL}")

    return templates

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}✘ Aborted.{Style.RESET_ALL}")
        sys.exit(0)
