from __future__ import annotations
import os
import json
from typing import List, Union
from pathlib import Path

from .cli import ScoopCLI
from .manifest import Manifest
from .bucket import Bucket
from .models import ScoopExport


USER_HOME = os.path.expanduser('~')
SCOOP_HOME = os.path.join(USER_HOME, 'scoop')


class Scoop:

    def __init__(self, home_dir: str = SCOOP_HOME):
        self.home_dir = home_dir
        self.cli = ScoopCLI()

    def _get_local_buckets(self) -> List[Bucket]:
        buckets = []
        for bucket in Path(SCOOP_HOME).glob('buckets/*'):
            buckets.append(Bucket(bucket))
        return buckets

    def search(self, query: str, update: bool = False) -> List[Manifest]:
        if update:
            self.cli.update()
        manifests = []
        buckets = self._get_local_buckets()
        for bucket in buckets:
            for manifest in bucket.apps():
                if query.lower() in manifest.name.lower():
                    manifests.append(manifest)
        return manifests

    def _export(self) -> ScoopExport:
        return json.loads(self.cli.export())

    def list(self) -> List[Manifest]:
        apps = []
        for app in self._export()['apps']:
            try:
                apps.append(Manifest(Path(self.home_dir) / 'apps' /
                            app['Name'] / app['Version'] / 'manifest.json'))
            except TypeError:
                # TODO: handle this
                pass
        return apps

    def is_installed(self, app: Union[str, Manifest]) -> bool:
        if isinstance(app, Manifest):
            app = app.name
        return app in [app.name for app in self.list()]

    def install(self, app: Union[str, Manifest]) -> None:
        if self.is_installed(app):
            raise Exception(f'{app} is already installed')
        if isinstance(app, Manifest):
            app = str(app._path)
        self.cli.install(app)

    def uninstall(self, app: Union[str, Manifest]) -> None:
        if not self.is_installed(app):
            raise Exception(f'{app} is not installed')
        if isinstance(app, Manifest):
            app = app.name
        self.cli.uninstall(app)
