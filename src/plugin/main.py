from typing import List
from pyflowlauncher import Plugin
from pyflowlauncher.result import send_results

from .commands import search, app_list
from .results import menu_results, context_menu_results

plugin = Plugin()

COMMANDS = {
    "search": search,
    "list": app_list
}


def menu(query: str):
    return send_results(menu_results(COMMANDS))


@plugin.on_method
def query(query: str):
    command = query.split(" ")[0]
    return COMMANDS.get(command, menu)(query)


@plugin.on_method
def context_menu(data: List):
    results = context_menu_results(data[0])
    return send_results(results)
