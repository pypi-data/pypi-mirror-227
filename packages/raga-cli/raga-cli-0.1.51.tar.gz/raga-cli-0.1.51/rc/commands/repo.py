import argparse
import logging

from rc.cli.command import CmdBase
from rc.exceptions import RcException

logger = logging.getLogger(__name__)

class RepoError(RcException):
    def __init__(self, msg):
        super().__init__(msg)
 

"""
----------------------------
***Repo Name Validation***
----------------------------
Bucket names should not contain upper-case letters
Bucket names should not contain underscores (_)
Bucket names should not end with a dash
Bucket names should be between 3 and 63 characters long
Bucket names cannot contain dashes next to periods (e.g., my-.bucket.com and my.-bucket are invalid)
Bucket names cannot contain periods - Due to our S3 client utilizing SSL/HTTPS, Amazon documentation indicates that a bucket name cannot contain a period, otherwise you will not be able to upload files from our S3 browser in the dashboard.
"""   


class CmdRepo(CmdBase):
    def validate_args(self) -> None:
        from rc.exceptions import InvalidArgumentError

        args = self.args
        name = args.name.lower()
        if args.create:
            if self.args.tag:
                if self.args.tag not in ['dataset', 'model']:
                    raise InvalidArgumentError("tag should be either dataset or model")
            else:
                raise InvalidArgumentError("the following argument is required: -tag/--tag when using -c/--create")
        for c in name:        
            if c == '_':
                raise InvalidArgumentError(f"repo name contains invalid (_) characters. Name: {name}")
            if len(name) <3 or len(name)>63:
                raise InvalidArgumentError("repo names should be between 3 and 63 characters long")
        self.args.name = name
        

    def run(self): 
        from rc.exceptions import RcException, InvalidArgumentError
        from rc.apis.repos import RcRepo, RcRepoCommit
        from rc.git import Git
        from rc.dvc import DVC
        from halo import Halo
        try:
            self.validate_args()
        except InvalidArgumentError:
            logger.exception("")
            return 1 

        try:       
            if self.args.create:
                with Halo(text=f"Creating '{self.args.name}'...", spinner='dots') as sp:
                    git = Git(self.config)
                    dvc = DVC(self.config)
                    self.repo.create(
                        self.args.name,
                        self.args.tag,
                        self.config,
                        RcRepo(self.config, self.args.name, self.args.tag),
                        RcRepoCommit(self.config, self.args.name, dvc, git),
                        git,
                        dvc,
                        sp
                        )
            if self.args.clone:
                with Halo(text=f"Cloning into '{self.args.name}'...", spinner='dots') as sp:
                    git = Git(self.config)
                    dvc = DVC(self.config)
                    self.repo.clone(
                        self.args.name,
                        self.config,
                        RcRepo(self.config, self.args.name, self.args.tag),
                        RcRepoCommit(self.config, self.args.name, dvc, git),
                        git,
                        dvc,
                        sp
                        )                                  
        except RcException:
            logger.exception("")
            return 1
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Create a new repository."

    repo_parser = subparsers.add_parser(
        "repo",
        parents=[parent_parser],
        description=REPO_HELP,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    create_clone_group = repo_parser.add_mutually_exclusive_group(required=True)
    create_clone_group.add_argument(
        "-c",
        "--create",
        action="store_true",
        default=False,
        help="Create new repo",
    )

    create_clone_group.add_argument(
        "-cln",
        "--clone",
        action="store_true",
        default=False,
        help="Clone new repo",
    )

    repo_parser.add_argument(
        "-n", 
        "--name", 
        required=True,
        nargs="?", 
        help="Name of the repo",
    )

    repo_parser.add_argument(
        "-tag", 
        "--tag", 
        nargs="?", 
        help="Tag of the repo",
    )

    repo_parser.add_argument(
        "-p", 
        "--profile", 
        action="store_true",
        default=False,
        help="Config profile",
    )

    repo_parser.set_defaults(func=CmdRepo)
