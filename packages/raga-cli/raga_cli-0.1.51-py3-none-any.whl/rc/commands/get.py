import argparse
import logging
from rc.cli.command import CmdBase

logger = logging.getLogger(__name__)

class CmdGet(CmdBase):   
        
    def run(self):
        from rc.exceptions import RcException, InvalidArgumentError
        from rc.apis.repos import RcRepo, RcRepoCommit, RepoLock
        from rc.git import Git
        from rc.dirs import get_dir_name
        from rc.dvc import DVC
        from halo import Halo
  
        repo_name = get_dir_name()
        try:   
            with Halo(text=f"Processing...", spinner='dots') as sp:  
                git = Git(self.config)
                dvc = DVC(self.config)
                repo = RcRepo(self.config, repo_name)
                self.repo.get(
                        repo_name,
                        self.args.commit_version,
                        self.config,
                        repo,
                        RcRepoCommit(self.config, repo ,dvc, git),
                        RepoLock(self.config, repo_name),
                        git,
                        dvc,
                        sp
                        )                                
        except RcException:
            logger.exception("")
            return 1 
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Get File or folder. Use: `rc get`"
    REPO_DESCRIPTION = (
        "Get File or folder. Use: `rc get`"
    )

    repo_parser = subparsers.add_parser(
        "get",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    repo_parser.add_argument(
        "-cv", 
        "--commit-version", 
        nargs="?", 
        default=None,
        type=int,
        help="Repo commit version",
    )

    repo_parser.add_argument(
        "-p", 
        "--profile", 
        action="store_true",
        default=False,
        help="Config profile",
    )
    repo_parser.set_defaults(func=CmdGet)