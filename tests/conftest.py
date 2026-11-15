import json

import pytest

import commands
from scoop.cli import ScoopCLI
from scoop.scoop import Scoop

BUCKETS = {
    "main": {
        "git": {"version": "2.47.1", "description": "Distributed version control system", "homepage": "https://gitforwindows.org"},
        "git-lfs": {"version": "3.6.0", "description": "Git extension for versioning large files", "homepage": "https://git-lfs.com"},
        "7zip": {"version": "24.09", "description": "A multi-format file archiver with high compression ratios", "homepage": "https://www.7-zip.org"},
        "elasticsearch": {"version": "8.16.0", "description": "Distributed search and analytics engine"},
    },
    "extras": {
        "gitkraken": {"version": "10.5.0", "description": "Git GUI client", "homepage": "https://www.gitkraken.com"},
    },
}
INSTALLED = {"git": "2.47.1", "7zip": "24.09"}


class FakeRunner:
    def __init__(self, outputs=None):
        self.calls = []
        self.outputs = outputs or {}

    def __call__(self, cmd):
        self.calls.append(cmd)
        return self.outputs.get(tuple(cmd[1:]), "")


def export_output(installed):
    return json.dumps({
        "buckets": [{"Name": name, "Source": "", "Updated": {}, "Manifests": len(apps)} for name, apps in BUCKETS.items()],
        "apps": [
            {"Name": name, "Version": version, "Source": "main", "Info": "", "Updated": "2026-11-01 10:00:00"}
            for name, version in installed.items()
        ],
    })


@pytest.fixture
def scoop_home(tmp_path):
    for bucket, apps in BUCKETS.items():
        bucket_dir = tmp_path / "buckets" / bucket / "bucket"
        bucket_dir.mkdir(parents=True)
        for name, manifest in apps.items():
            (bucket_dir / f"{name}.json").write_text(json.dumps(manifest), encoding="utf-8")
    for name, version in INSTALLED.items():
        app_dir = tmp_path / "apps" / name / version
        app_dir.mkdir(parents=True)
        manifest = BUCKETS["main"][name]
        (app_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return tmp_path


@pytest.fixture
def runner():
    return FakeRunner({("export",): export_output(INSTALLED)})


@pytest.fixture
def scoop(scoop_home, runner, monkeypatch):
    fake = Scoop(str(scoop_home), ScoopCLI(runner))
    monkeypatch.setattr(commands, "scoop", lambda: fake)
    return fake
