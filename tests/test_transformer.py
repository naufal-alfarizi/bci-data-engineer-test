import pytest
from transformers.address_transformer import transform


def test_transform_enriches(monkeypatch):
    monkeypatch.setattr(
        "transformers.address_transformer.get_structured_address",
        lambda addr: type(
            "SA",
            (),
            {"full_address": f"FULL {addr}", "latitude": 1.23, "longitude": 4.56},
        )(),
    )

    recs = list(transform(iter([{"project_address": "A", "x": 1}])))
    assert recs[0]["geocoded_address"] == "FULL A"
    assert recs[0]["latitude"] == pytest.approx(1.23)
    assert recs[0]["longitude"] == pytest.approx(4.56)


def test_transform_handles_missing_address():
    recs = list(transform(iter([{"x": 1}])))
    assert recs[0]["geocoded_address"] is None


def test_transform_continues_on_error(monkeypatch):
    def boom(_):
        raise Exception("fail")

    monkeypatch.setattr("transformers.address_transformer.get_structured_address", boom)
    recs = list(transform(iter([{"project_address": "A"}])))
    assert recs[0]["geocoded_address"] is None