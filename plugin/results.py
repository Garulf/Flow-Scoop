from typing import Dict, Generator, List

from plugin.scoop.bucket import Manifest
from pyflowlauncher.plugin import Method
from pyflowlauncher.api import open_url, open_directory
from pyflowlauncher.result import Result
from pyflowlauncher.icons import ICONS
from .actions import install_app, uninstall_app, update_app


def menu_results(commands: Dict[str, Method]) -> Generator[Result, None, None]:
    for command in commands:
        yield Result(
            Title=command,
            IcoPath="../icon.jpg",
        )


def manifest_results(manifests: List[Manifest]) -> Generator[Result, None, None]:
    for manifest in manifests:
        try:
            yield Result(
                Title=f"{manifest.name} ({manifest.version})",
                SubTitle=str(manifest.description),
                IcoPath=ICONS["2566"],
                JsonRPCAction=install_app(str(manifest._path)),
                ContextData=[str(manifest._path)]
            )
        except Exception:
            pass


def context_menu_results(manifest_path: str) -> Generator[Result, None, None]:
    manifest = Manifest(manifest_path)
    is_installed = manifest.is_installed
    if is_installed:
        yield Result(
            Title=f"Uninstall {manifest.name}",
            IcoPath=ICONS["checkupdate"],
            JsonRPCAction=uninstall_app(manifest.name),
        )
        yield Result(
            Title=f'Update {manifest.name}',
            IcoPath=ICONS["checkupdate"],
            JsonRPCAction=update_app(manifest.name),
        )
        yield Result(
            Title='Reveal in Explorer',
            IcoPath=ICONS["explorer"],
            JsonRPCAction=open_directory(
                str(manifest._path.parent), str(manifest._path)),
        )
    else:
        yield Result(
            Title=f"Install {manifest.name}",
            IcoPath=ICONS["install"],
            JsonRPCAction=install_app(str(manifest._path)),
        )
    if manifest.homepage:
        yield Result(
            Title='Open homepage',
            SubTitle=manifest.homepage,
            IcoPath=ICONS["url"],
            JsonRPCAction=open_url(manifest.homepage),
        )
