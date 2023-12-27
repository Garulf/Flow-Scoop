from plugin.results import manifest_results
from pyflowlauncher import send_results
from .scoop.scoop import Scoop


def search(query: str):
    manifests = Scoop().search(query.replace("search", "").strip())[:25]
    return send_results(manifest_results(manifests))


def app_list(query: str):
    apps = Scoop().list()
    return send_results(manifest_results(apps))
