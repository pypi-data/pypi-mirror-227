from git.cmd import Git
from utils.data import CacheKey


class GitCli(CacheKey):
    def update_proj(self, work_dir: str) -> str:
        try:
            g = Git(work_dir)
            g.pull()
        except Exception as err:
            return f"{err}"
        return ""
