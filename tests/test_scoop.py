import subprocess

from scoop.cli import ScoopCLI, run_scoop
from scoop.manifest import Manifest


def test_search_matches_app_names_in_every_local_bucket(scoop):
    names = sorted(manifest.name for manifest in scoop.search("GIT"))
    assert names == ["git", "git-lfs", "gitkraken"]


def test_search_reads_buckets_from_the_scoop_home(scoop, scoop_home):
    (manifest,) = scoop.search("7zip")
    assert manifest.path == scoop_home / "buckets" / "main" / "bucket" / "7zip.json"
    assert manifest.version == "24.09"
    assert not manifest.is_installed


def test_list_reads_installed_manifests_from_scoop_export(scoop, scoop_home, runner):
    apps = scoop.list()
    assert runner.calls == [["scoop", "export"]]
    assert [app.path for app in apps] == [
        scoop_home / "apps" / "git" / "2.47.1" / "manifest.json",
        scoop_home / "apps" / "7zip" / "24.09" / "manifest.json",
    ]
    assert [app.name for app in apps] == ["git", "7zip"]
    assert all(app.is_installed for app in apps)


def test_manifest_defaults(tmp_path):
    path = tmp_path / "bare.json"
    path.write_text('{"version": "1.0"}', encoding="utf-8")
    manifest = Manifest(path)
    assert manifest.description == "UNKNOWN"
    assert manifest.homepage is None


def test_cli_commands():
    calls = []
    cli = ScoopCLI(lambda cmd: calls.append(cmd) or "")
    cli.install("git")
    cli.uninstall("git")
    cli.update()
    cli.update("git")
    cli.search("git")
    cli.list()
    assert calls == [
        ["scoop", "install", "git"],
        ["scoop", "uninstall", "git"],
        ["scoop", "update"],
        ["scoop", "update", "git"],
        ["scoop", "search", "git"],
        ["scoop", "list"],
    ]


def test_run_scoop_runs_through_the_shell_without_the_plugin_stdin(monkeypatch):
    seen = {}

    class FakePopen:
        def __init__(self, cmd, **kwargs):
            seen["cmd"] = cmd
            seen.update(kwargs)

        def communicate(self):
            return b'  {"apps": []}\r\n', b""

    monkeypatch.setattr(subprocess, "Popen", FakePopen)
    assert run_scoop(["scoop", "export"]) == '{"apps": []}'
    assert seen["cmd"] == ["scoop", "export"]
    assert seen["shell"] is True
    assert seen["stdin"] is subprocess.DEVNULL
    assert seen["stdout"] is subprocess.PIPE
