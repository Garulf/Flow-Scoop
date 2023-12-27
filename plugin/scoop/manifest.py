import json
from pathlib import Path
from typing import Optional, Union


class Manifest:

    def __init__(self, path: Union[str, Path]):
        self._path = Path(path)
        self._data = None

    def __repr__(self) -> str:
        return f'<App {self.name}>'

    def _load(self):
        with open(self._path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    @property
    def _loaded_data(self):
        if self._data is None:
            self._load()
        return self._data

    @property
    def name(self) -> str:
        if 'apps' in self._path.parts:
            return self._path.parts[-3]
        return self._path.stem

    @property
    def description(self) -> str:
        return self._loaded_data.get('description', 'UNKNOWN')

    @property
    def version(self) -> str:
        return self._loaded_data['version']

    @property
    def homepage(self) -> str:
        return self._loaded_data.get('homepage')

    @property
    def is_installed(self) -> bool:
        return self._path.stem == 'manifest'
