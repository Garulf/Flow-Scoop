from typing import List

from scoop.manifest import Manifest
from scoop.scoop import Scoop

SEARCH_LIMIT = 25


def scoop() -> Scoop:
    return Scoop()


def search(query: str) -> List[Manifest]:
    terms = query.split(" ", 1)[1] if " " in query else ""
    return scoop().search(terms.strip())[:SEARCH_LIMIT]


def app_list(query: str) -> List[Manifest]:
    return scoop().list()
