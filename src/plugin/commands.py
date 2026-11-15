from typing import List

from scoop.manifest import Manifest
from scoop.scoop import Scoop

SEARCH_LIMIT = 25


def scoop() -> Scoop:
    return Scoop()


def search(query: str) -> List[Manifest]:
    return scoop().search(query.replace("search", "").strip())[:SEARCH_LIMIT]


def app_list(query: str) -> List[Manifest]:
    return scoop().list()
