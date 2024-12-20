#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, requests, argparse
from difflib import get_close_matches
from typing import Optional, List
from .cache import load_from_cache, save_to_cache
from .search import handle_search
from .version import __version__
from colorama import init, Fore, Style

init(autoreset=True)

def main():
    parser = construct_parser()
    args = parser.parse_args()
    
    templates = load_templates()

    if args.command == "list":        
        for template in templates:
            print(f"{Fore.WHITE}{template['name']}{Style.RESET_ALL}")

        sys.exit(0)

    if args.command == "search":
        # only pass the template names to the search function
        template_id = handle_search("Search for a template", [t["name"] for t in templates])
        args.template = [templates[template_id]["name"]]
        args.command = "use"
        
        confirm = get_bool_answer(f"\n{Fore.YELLOW}Apply template:{Style.RESET_ALL} {', '.join(args.template)}")
        if not confirm:
            print(f"{Fore.RED}✘ Aborting...{Style.RESET_ALL}")
            sys.exit(0)


    if args.command == "use":
        print(f"{Fore.YELLOW}Applying template(s):{Style.RESET_ALL} {', '.join(args.template)}")

        gitignore_content = []
        templates_found = []

        for template_name in args.template:
            template = next((t for t in templates if t["name"].lower() == template_name.lower()), None)
            if template:
                templates_found.append(template["name"])
                
                template_content = fetch_template(template["download_url"])
                if template_content is None or template_content == "":
                    print(f"{Fore.RED}✘ Error fetching template {template['name']}{Style.RESET_ALL}")
                    continue

                gitignore_content.append(f"### {template['name'].upper()} ###")
                gitignore_content.append("")
                gitignore_content.append("")
                gitignore_content.extend(template_content.splitlines())
            else:
                print(f"{Fore.RED}Template {Style.RESET_ALL}{template_name}{Fore.RED} not found{Style.RESET_ALL}")
                sys.exit(1)

        if not templates_found:
            print(f"{Fore.RED}✘ No valid templates found{Style.RESET_ALL}")
            sys.exit(1)

        if os.path.exists(".gitignore") and os.path.getsize(".gitignore") > 0:
            action = handle_search(f"{Fore.YELLOW}A .gitignore file already exists. Select how to handle it?{Style.RESET_ALL}",
                                   ["Overwrite", "Append", "Abort"])
            
            print("\n")
            if action == 0:
                print(f"{Fore.YELLOW}Overwriting .gitignore file...{Style.RESET_ALL}")
            
            elif action == 1:
                print(f"{Fore.YELLOW}Appending to .gitignore file...{Style.RESET_ALL}")
                with open(".gitignore", "r") as f:
                    gitignore_content = f.read().splitlines() + gitignore_content
            elif action == 2:
                print(f"{Fore.RED}✘ Aborting...{Style.RESET_ALL}")
                sys.exit(0)

        with open(".gitignore", "w") as f:
            f.write(f"\n".join(gitignore_content))

        print(f"{Fore.GREEN}✔ .gitignore file created updated with {len(templates_found)} template(s){Style.RESET_ALL}")
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

    parser.add_argument("--version", action="version", version="generate-gitignore: " + __version__)

    subparsers = parser.add_subparsers(dest='command')
    
    list_parser = subparsers.add_parser('list', help='List available .gitignore templates')
    
    search_parser = subparsers.add_parser('search', help='Search for a specific .gitignore template')
    
    use_parser = subparsers.add_parser('use', help='Use specific .gitignore template(s)')
    use_parser.add_argument('template', nargs='+', help='Template name(s) to use')


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
        print(f"\n{Fore.RED}✘ Aborting...{Style.RESET_ALL}")
        sys.exit(0)
