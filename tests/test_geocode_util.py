import os
import pytest
from integrations.geocode_util import GeocodingError, StructuredAddress, get_structured_address


class DummyResponse:
    def __init__(self, status_code: int, json_data=None, text: str = ""):
        self.status_code = status_code
        self._json_data = json_data
        self.text = text

    def json(self):
        if isinstance(self._json_data, Exception):
            raise self._json_data
        return self._json_data


def test_get_structured_address_success(monkeypatch):
    def fake_get(url, params=None, timeout=None):
        assert "locationiq.com" in url
        assert params["q"] == "Bahnhofquai 8"
        return DummyResponse(
            200,
            [
                {
                    "display_name": "Bahnhofquai 8, 8001 Zürich, Switzerland",
                    "lat": "47.3769",
                    "lon": "8.5417",
                }
            ],
        )

    monkeypatch.setattr("integrations.geocode_util.requests.get", fake_get)
    os.environ["LOCATIONIQ_API_KEY"] = "test-key"

    out = get_structured_address("Bahnhofquai 8")
    assert isinstance(out, StructuredAddress)
    assert out.full_address.startswith("Bahnhofquai 8")
    assert out.latitude == pytest.approx(47.3769)
    assert out.longitude == pytest.approx(8.5417)


def test_get_structured_address_empty_raises():
    with pytest.raises(ValueError):
        get_structured_address("   ")


def test_get_structured_address_no_results(monkeypatch):
    monkeypatch.setattr(
        "integrations.geocode_util.requests.get",
        lambda *a, **k: DummyResponse(200, []),
    )
    os.environ["LOCATIONIQ_API_KEY"] = "test-key"
    with pytest.raises(GeocodingError):
        get_structured_address("Some unknown place")


def test_get_structured_address_http_error(monkeypatch):
    monkeypatch.setattr(
        "integrations.geocode_util.requests.get",
        lambda *a, **k: DummyResponse(429, {"error": "rate limit"}, text="rate"),
    )
    os.environ["LOCATIONIQ_API_KEY"] = "test-key"
    with pytest.raises(GeocodingError) as e:
        get_structured_address("Bahnhofquai 8")
    assert "429" in str(e.value)


def test_get_structured_address_missing_api_key(monkeypatch):
    monkeypatch.setattr(
        "integrations.geocode_util.requests.get",
        lambda *a, **k: DummyResponse(200, []),
    )
    os.environ.pop("LOCATIONIQ_API_KEY", None)
    with pytest.raises(GeocodingError):
        get_structured_address("Bahnhofquai 8")
