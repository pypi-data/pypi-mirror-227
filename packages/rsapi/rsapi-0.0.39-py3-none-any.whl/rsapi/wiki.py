import re
import typing

import requests
import typing_extensions

from rsapi import USER_AGENT

API_URL = "https://prices.runescape.wiki"
MAPPING_PATH = "api/v1/osrs/mapping"
LATEST_PATH = "api/v1/osrs/latest"


class Item(typing.TypedDict, total=False):
    examine: str
    id: int
    members: bool
    value: int
    icon: str
    name: str
    lowalch: typing.Optional[int]
    highalch: typing.Optional[int]
    limit: typing.Optional[int]


class PriceLatest(typing.TypedDict, total=False):
    id: int
    high: int
    highTime: int
    low: int
    lowTime: int


def _request(path: str, **params) -> dict:
    resp = requests.get(
        f"{API_URL}/{path}",
        params=params,
        headers={
            "User-Agent": USER_AGENT,
        }
    )
    resp.raise_for_status()
    return resp.json()


def items(**filters: typing_extensions.Unpack[Item]) -> typing.Iterable[Item]:
    for item in _request(MAPPING_PATH):
        for key, value in filters.items():
            if key not in item:
                continue
            if isinstance(value, int):
                if item[key] == value:
                    yield item
            elif isinstance(value, str):
                if str(item[key]).lower() == value.lower():
                    yield item
                elif re.search(value, str(item[key]), flags=re.IGNORECASE):
                    yield item
            else:
                raise TypeError("Bad argument type")


def price_latest(
    **filters: typing_extensions.Unpack[Item]
) -> typing.Iterable[PriceLatest]:
    for item in items(**filters):
        for price in _request(LATEST_PATH, id=item["id"]).values():
            yield PriceLatest({
                "id": item["id"],
                **price.get(str(item["id"])),
            })
