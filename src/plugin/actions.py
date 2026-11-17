from pyflowlauncher.api import shell_run
from pyflowlauncher.command import Command


def _run_command(command: str) -> Command:
    return shell_run(f'start cmd.exe /K "{command}"')


def install_app(app_path: str) -> Command:
    return _run_command(f'scoop install {app_path}')


def uninstall_app(app_name: str) -> Command:
    return _run_command(f'scoop uninstall {app_name}')


def update_app(app_name: str) -> Command:
    return _run_command(f'scoop update {app_name}')
