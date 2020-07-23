import os
from contextlib import ContextDecorator


class SetEnvVarContext(ContextDecorator):
    def __init__(self, var, val):
        self.var = var
        self.val = val

    def __enter__(self):
        os.environ[self.var] = self.val

    def __exit__(self, *exc):
        del os.environ[self.var]
