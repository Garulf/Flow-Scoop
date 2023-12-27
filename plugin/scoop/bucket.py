from __future__ import annotations
from pathlib import Path
from typing import List

from .manifest import Manifest


class Bucket:

    def __init__(self, path: Path):
        self.path = path

    @property
    def name(self) -> str:
        return self.path.name

    def apps(self) -> List[Manifest]:
        return [Manifest(manifest) for manifest in self.path.glob('bucket/*.json')]
