from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass, field
from pathlib import Path

from plugin.scoop.bucket import Manifest

if TYPE_CHECKING:
    from plugin.scoop.scoop import Scoop


@dataclass
class InstalledApp:
    Name: str
    Source: str
    Info: str
    Version: str
    Updated: str
    _scoop: Scoop = field(repr=False)

    @property
    def manifest(self) -> Manifest:
        return Manifest(Path(self._scoop.home_dir) / 'apps' / self.Name / self.Version / 'manifest.json')
