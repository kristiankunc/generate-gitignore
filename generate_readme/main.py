#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import json
from difflib import get_close_matches
from typing import Optional, List
import requests
import argparse
from generate_readme.cache import load_from_cache, save_to_cache
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def main():
    parser = construct_parser()
    args = parser.parse_args()
    
    if args.list:
        templates = load_templates()
        
        for template in templates:
            print(f"{Fore.WHITE}{template['name']}{Style.RESET_ALL}")

        sys.exit(0)

    if args.search:
        templates = load_templates()

        matches = find_closest_match(args.search, [template["name"] for template in templates])
        if matches:
            print(f"{Fore.WHITE}Found the following matches: {', '.join([f'{Fore.BLUE}' + match + f'{Style.RESET_ALL}' for match in matches])}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}🗙 No match found{Style.RESET_ALL}")

        sys.exit(0)

    if args.use:
        templates = load_templates()

        template = next((template for template in templates if template["name"].lower() == args.use.lower()), None)
        if template:
            print(f"{Fore.GREEN}Applying {template['name']}...{Style.RESET_ALL}")

            # check if .gitignore already exists and is not empty
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

    # DEV ONLY
    with open("templates.json", "r") as f:
        return json.load(f)
    
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

    parser.add_argument("--list", action="store_true", help="List available .gitignore templates")
    parser.add_argument("--search", help="Search for a specific .gitignore template")
    parser.add_argument("--use", help="Use a specific .gitignore template")


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

    :param prompt: The prompt to display to the user.
    :return: True if the user answers 'yes', False if the user answers 'no', and None if the input is invalid.
    """

    answer = input(f"{prompt} (yY/nN): ").lower()
    if answer in ["y", "yes"]:
        return True
    elif answer in ["n", "no"]:
        return False
    else:
        print(f"{Fore.RED}Invalid input. Please enter 'yes' or 'no'.{Style.RESET_ALL}")
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
    main()
