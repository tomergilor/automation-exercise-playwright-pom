import json
from pathlib import Path
from typing import Any

class DataLoader:
    @staticmethod
    def load_json(path: str | Path) -> list[dict[str, Any]]:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Data file was not found: {file_path}")
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Data file must contain a list of test cases")
        return data
