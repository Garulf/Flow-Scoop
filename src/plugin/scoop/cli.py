import subprocess
from typing import Callable, List, Optional

PATH = 'scoop'

Runner = Callable[[List[str]], str]


def run_scoop(cmd: List[str]) -> str:
    proc = subprocess.Popen(
        cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = proc.communicate()
    return out.decode('utf-8').strip()


class ScoopCLI:
    INSTALL = 'install'
    UNINSTALL = 'uninstall'
    SEARCH = 'search'
    LIST = 'list'
    UPDATE = 'update'

    def __init__(self, runner: Runner = run_scoop, path: str = PATH):
        self._runner = runner
        self._path = path

    def _cmd(self, cmd: List[str]) -> str:
        return self._runner([self._path] + cmd)

    def search(self, query: str) -> str:
        return self._cmd([self.SEARCH, query])

    def update(self, arg: Optional[str] = None) -> str:
        args = [self.UPDATE]
        if arg:
            args.append(arg)
        return self._cmd(args)

    def export(self) -> str:
        return self._cmd(['export'])

    def list(self) -> str:
        return self._cmd([self.LIST])

    def install(self, app: str) -> str:
        return self._cmd([self.INSTALL, app])

    def uninstall(self, app: str) -> str:
        return self._cmd([self.UNINSTALL, app])
