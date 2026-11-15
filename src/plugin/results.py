from typing import Iterable, Iterator

from pyflowlauncher import Result
from pyflowlauncher.api import open_directory, open_url
from pyflowlauncher.icons import Icons

from actions import install_app, uninstall_app, update_app
from scoop.manifest import Manifest

PLUGIN_ICON = "icon.png"


def menu_results(commands: Iterable[str]) -> Iterator[Result]:
    for command in commands:
        yield Result(title=command, icon=PLUGIN_ICON)


def manifest_results(manifests: Iterable[Manifest], icons: Icons) -> Iterator[Result]:
    for manifest in manifests:
        try:
            title = f"{manifest.name} ({manifest.version})"
            description = str(manifest.description)
        except (OSError, ValueError, KeyError):
            continue
        yield Result(
            title=title,
            subtitle=description,
            icon=getattr(icons, "2566"),
            context_data=[str(manifest.path)],
        ).add_action(install_app(str(manifest.path)))


def context_menu_results(manifest_path: str, icons: Icons) -> Iterator[Result]:
    manifest = Manifest(manifest_path)
    if manifest.is_installed:
        yield Result(
            title=f"Uninstall {manifest.name}",
            icon=icons.checkupdate,
        ).add_action(uninstall_app(manifest.name))
        yield Result(
            title=f"Update {manifest.name}",
            icon=icons.checkupdate,
        ).add_action(update_app(manifest.name))
        yield Result(
            title="Reveal in Explorer",
            icon=icons.explorer,
        ).add_action(open_directory(str(manifest.path.parent), str(manifest.path)))
    else:
        yield Result(
            title=f"Install {manifest.name}",
            icon=icons.install,
        ).add_action(install_app(str(manifest.path)))
    if manifest.homepage:
        yield Result(
            title="Open homepage",
            subtitle=manifest.homepage,
            icon=icons.url,
        ).add_action(open_url(manifest.homepage))
