import json
from typing import Any, Dict

class JSONDataManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = {}

    def load_data(self):
        try:
            with open(self.filepath) as file:
                self.data = json.load(file)
                return self.data
        except FileNotFoundError:
            print(f"No such file: '{self.filepath}'")
        except json.JSONDecodeError:
            print("Failed to decode JSON")

    def save_data(self, filepath: str = None):
        if filepath is None:
            filepath = self.filepath  # Default to the original file
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except IOError:
            print(f"Could not write to file: '{filepath}'")

