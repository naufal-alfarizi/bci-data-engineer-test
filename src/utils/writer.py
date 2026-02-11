from __future__ import annotations
import json
import os
from pathlib import Path
from typing import Iterable, Mapping, Union

def write_json(
    data: Iterable[Mapping],
    path: Union[str, os.PathLike],
    *,
    filename: str = "enriched_output.json",
) -> Path:
    """
    Writes an iterator of dicts to a JSON file.
    Args:
        data (iterable): An iterator of dictionaries to write to the JSON file.
        path (str): The file path where the JSON data will be written.
    """

    p = Path(path)
    out_file = p
    if p.exists() and p.is_dir() or str(p).endswith(os.sep) or (not p.suffix):
        p.mkdir(parents=True, exist_ok=True)
        out_file = p / filename
    else:
        out_file.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for rec in data:
        if not isinstance(rec, Mapping):
            raise ValueError(f"write_json expects mapping records, got {type(rec)}")
        records.append(dict(rec))

    with out_file.open("w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return out_file
