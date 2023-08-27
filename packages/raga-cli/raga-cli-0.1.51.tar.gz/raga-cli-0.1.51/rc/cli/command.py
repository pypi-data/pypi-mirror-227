import logging
import os
from abc import ABC, abstractmethod

from rc.config import Config, CoreConfig


logger = logging.getLogger(__name__)


class CmdBase(ABC):
    def __init__(self, args):
        from rc.repo import Repo
        from rc.profile import config_profile
        profile = getattr(args, "profile", None) if args.profile else config_profile()
        self.repo: "Repo" = Repo()
        self.config: "Config" =  Config(profile=profile)
        self.args = args
    def do_run(self):
        return self.run()
            
    @abstractmethod
    def run(self):
        pass


