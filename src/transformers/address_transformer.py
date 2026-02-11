from __future__ import annotations
from typing import Dict, Iterator
from integrations.geocode_util import GeocodingError, StructuredAddress, get_structured_address


def transform(address_iter: Iterator[Dict]) -> Iterator[Dict]:
    """
    Transforms an iterator of address dictionaries by enriching each address.
    Yields enriched addresses one by one.
    """

    for record in address_iter:
        if not isinstance(record, dict):
            raise ValueError(f"transform expects dict records, got {type(record)}")

        addr = record.get("project_address")

        enriched: Dict = dict(record)
        if not addr:
            enriched.update({"geocoded_address": None, "latitude": None, "longitude": None})
            yield enriched
            continue

        try:
            sa: StructuredAddress = get_structured_address(str(addr))
            enriched.update(
                {
                    "geocoded_address": sa.full_address,
                    "latitude": sa.latitude,
                    "longitude": sa.longitude,
                }
            )
        except (GeocodingError, ValueError, Exception):
            enriched.update({"geocoded_address": None, "latitude": None, "longitude": None})

        yield enriched
