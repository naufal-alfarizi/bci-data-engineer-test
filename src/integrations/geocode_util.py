from __future__ import annotations
from dataclasses import dataclass
import os
from typing import Optional
import requests
from dotenv import load_dotenv

class GeocodingError(RuntimeError):
    """Raised when geocoding fails due to configuration, network, or API issues."""


@dataclass(frozen=True)
class StructuredAddress:
    full_address: str
    latitude: float
    longitude: float


def _get_api_key() -> str:
    # Load .env if present (helps local development and the provided Docker setup).
    load_dotenv(override=False)
    key = os.getenv("LOCATIONIQ_API_KEY")
    if not key:
        raise GeocodingError(
            "Missing LocationIQ API key. Set LOCATIONIQ_API_KEY (e.g., via .env)."
        )
    return key


def get_structured_address(
    partial_address: str,
    *,
    country: Optional[str] = None,
    timeout_s: float = 10.0,
) -> StructuredAddress:
    """
    Given a partial address, returns the full structured address using LocationIQ API.
    """

    if not partial_address or not partial_address.strip():
        raise ValueError("partial_address must be a non-empty string")

    api_key = _get_api_key()

    params = {
        "key": api_key,
        "q": partial_address.strip(),
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }
    if country:
        params["countrycodes"] = country

    try:
        resp = requests.get(
            "https://us1.locationiq.com/v1/search",
            params=params,
            timeout=timeout_s,
        )
    except requests.RequestException as e:
        raise GeocodingError(f"Geocoding request failed: {e}") from e

    if resp.status_code != 200:
        msg = None
        try:
            msg = resp.json().get("error")
        except Exception:
            msg = None
        raise GeocodingError(
            f"Geocoding API error ({resp.status_code}): {msg or resp.text.strip()}"
        )

    try:
        payload = resp.json()
    except Exception as e:
        raise GeocodingError("Geocoding API returned non-JSON response") from e

    if not isinstance(payload, list) or not payload:
        raise GeocodingError(f"No geocoding results for address: {partial_address!r}")

    hit = payload[0]
    full = hit.get("display_name")
    lat = hit.get("lat")
    lon = hit.get("lon")

    if full is None or lat is None or lon is None:
        raise GeocodingError("Geocoding API response missing required fields")

    try:
        return StructuredAddress(full_address=str(full), latitude=float(lat), longitude=float(lon))
    except Exception as e:
        raise GeocodingError("Failed to parse latitude/longitude from API response") from e
