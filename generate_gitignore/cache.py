# -*- coding: utf-8 -*-

import json
import os
from platformdirs import user_cache_dir
from datetime import datetime

APP_NAME = "py-generate_readme"

def get_cache_file_path(filename: str) -> str:
    """
    Get the full path to a cache file for the application.

    :param filename: The name of the cache file (e.g., 'data.json').
    :return: The full path to the cache file.
    """
    cache_dir = user_cache_dir(APP_NAME)
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, filename)

def save_to_cache(data: dict, filename: str) -> None:
    """
    Save data to a cache file.

    :param data: The data to save (as a dictionary).
    :param filename: The name of the cache file.
    """
    cache_file = get_cache_file_path(filename)
    with open(cache_file, "w", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}\n")
        json.dump(data, f)

def load_from_cache(filename: str) -> dict:
    """
    Load data from a cache file.

    :param filename: The name of the cache file.
    :return: The loaded data (as a dictionary) or an empty dictionary if the cache doesn't exist or is older than 24 hours.
    """
    cache_file = get_cache_file_path(filename)
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            timestamp_str = f.readline().strip()
            timestamp = datetime.fromisoformat(timestamp_str)
            if (datetime.now() - timestamp).total_seconds() < 24 * 3600:
                return json.load(f)
    return {}