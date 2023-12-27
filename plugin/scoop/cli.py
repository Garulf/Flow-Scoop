import subprocess
from typing import List, Optional


PATH = 'scoop'


class ScoopCLI:
    INSTALL = 'install'
    UNINSTALL = 'uninstall'
    SEARCH = 'search'
    LIST = 'list'
    UPDATE = 'update'

    def _cmd(self, cmd: List[str], path: str = PATH) -> str:
        cmd = [path] + cmd
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        return out.decode('utf-8').strip()

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
