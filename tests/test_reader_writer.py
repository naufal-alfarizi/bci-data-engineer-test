import json
from pathlib import Path
import pytest
from utils.reader import read_json
from utils.writer import write_json


def test_read_json_from_file_list(tmp_path: Path):
    fp = tmp_path / "input.json"
    fp.write_text(json.dumps([{"a": 1}, {"a": 2}]), encoding="utf-8")

    recs = list(read_json(fp))
    assert recs == [{"a": 1}, {"a": 2}]


def test_read_json_from_dir(tmp_path: Path):
    (tmp_path / "1.json").write_text(json.dumps({"x": 1}), encoding="utf-8")
    (tmp_path / "2.json").write_text(json.dumps([{"x": 2}, {"x": 3}]), encoding="utf-8")

    recs = list(read_json(tmp_path))
    assert recs == [{"x": 1}, {"x": 2}, {"x": 3}]


def test_write_json_to_dir(tmp_path: Path):
    out_dir = tmp_path / "out"
    out_file = write_json([{"k": "v"}], out_dir)
    assert out_file.exists()

    loaded = json.loads(out_file.read_text(encoding="utf-8"))
    assert loaded == [{"k": "v"}]


def test_write_json_to_file(tmp_path: Path):
    out_file = tmp_path / "custom.json"
    returned = write_json([{"n": 1}], out_file)
    assert returned == out_file
    assert json.loads(out_file.read_text(encoding="utf-8")) == [{"n": 1}]


def test_read_json_raises_on_missing_path(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        list(read_json(tmp_path / "missing"))
