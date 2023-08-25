
class RcException(Exception):
    """Base class for all rc exceptions."""

    def __init__(self, msg, *args):
        assert msg
        self.msg = msg
        super().__init__(msg, *args)