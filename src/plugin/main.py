from typing import List

from pyflowlauncher import Plugin, api

from commands import app_list, search
from launcher import KEEP_OPEN, ScoopLauncher
from results import context_menu_results, manifest_results, menu_results

plugin = Plugin(launcher=ScoopLauncher())

COMMANDS = {
    "search": search,
    "list": app_list,
}


@plugin.on_method
def query(query: str):
    command = COMMANDS.get(query.split(" ")[0])
    if command is None:
        return menu_results(COMMANDS, plugin.launcher.action_keyword, change_query)
    return manifest_results(command(query))


@plugin.on_method
def context_menu(data: List):
    return context_menu_results(data[0], plugin.launcher.icons)


@plugin.on_method
async def change_query(query: str):
    await plugin.launcher.api.invoke(api.change_query(query))
    return KEEP_OPEN
