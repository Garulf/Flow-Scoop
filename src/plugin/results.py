from typing import Iterable, Iterator

from pyflowlauncher import Result
from pyflowlauncher.api import open_directory, open_url
from pyflowlauncher.icons import Icons
from pyflowlauncher.types import Method

from actions import install_app, uninstall_app, update_app
from scoop.manifest import Manifest

PLUGIN_ICON = "icon.png"


def menu_results(commands: Iterable[str], action_keyword: str, change_query: Method) -> Iterator[Result]:
    for command in commands:
        query = " ".join(filter(None, [action_keyword, command])) + " "
        yield Result(title=command, icon=PLUGIN_ICON).add_action(
            change_query, [query], dont_hide_after_action=True)


def manifest_results(manifests: Iterable[Manifest]) -> Iterator[Result]:
    for manifest in manifests:
        try:
            title = f"{manifest.name} ({manifest.version})"
            description = str(manifest.description)
        except (OSError, ValueError, KeyError):
            continue
        yield Result(
            title=title,
            subtitle=description,
            icon=PLUGIN_ICON,
            context_data=[str(manifest.path)],
        ).add_action(install_app(str(manifest.path)))


def context_menu_results(manifest_path: str, icons: Icons) -> Iterator[Result]:
    manifest = Manifest(manifest_path)
    if manifest.is_installed:
        yield Result(
            title=f"Uninstall {manifest.name}",
            icon=icons.delete,
        ).add_action(uninstall_app(manifest.name))
        yield Result(
            title=f"Update {manifest.name}",
            icon=icons.update,
        ).add_action(update_app(manifest.name))
        yield Result(
            title="Reveal in Explorer",
            icon=icons.folder,
        ).add_action(open_directory(str(manifest.path.parent), str(manifest.path)))
    else:
        yield Result(
            title=f"Install {manifest.name}",
            icon=PLUGIN_ICON,
        ).add_action(install_app(str(manifest.path)))
    if manifest.homepage:
        yield Result(
            title="Open homepage",
            subtitle=manifest.homepage,
            icon=icons.Browser,
        ).add_action(open_url(manifest.homepage))
