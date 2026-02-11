from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Dict, Iterator, Union

def read_json(path: Union[str, os.PathLike]) -> Iterator[Dict]:
    """
    Reads JSON files from a specified directory and yields each record.
    Args:
        path (str): The directory containing JSON files.
    Yields:
        dict: Each record from the JSON files.
    """

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Path does not exist: {p}")

    files = [p]
    if p.is_dir():
        files = sorted([fp for fp in p.iterdir() if fp.is_file() and fp.suffix.lower() == ".json"])

    for fp in files:
        with fp.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        if isinstance(payload, list):
            for item in payload:
                if not isinstance(item, dict):
                    raise ValueError(f"Expected dict items in JSON array in {fp}, got {type(item)}")
                yield item
        elif isinstance(payload, dict):
            yield payload
        else:
            raise ValueError(f"Unsupported JSON top-level type in {fp}: {type(payload)}")
