class BaseError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None


class UnexpectedError(BaseError):
    pass
