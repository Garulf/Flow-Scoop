from typing import List

from pyflowlauncher import FlowLauncherV2, Plugin

from commands import app_list, search
from results import context_menu_results, manifest_results, menu_results

plugin = Plugin(launcher=FlowLauncherV2())

COMMANDS = {
    "search": search,
    "list": app_list,
}


@plugin.on_method
def query(query: str):
    command = COMMANDS.get(query.split(" ")[0])
    if command is None:
        return menu_results(COMMANDS)
    return manifest_results(command(query))


@plugin.on_method
def context_menu(data: List):
    return context_menu_results(data[0], plugin.launcher.icons)
