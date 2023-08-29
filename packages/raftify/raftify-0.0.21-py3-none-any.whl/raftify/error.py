class UnknownError(Exception):
    pass


class LeaderNotFoundError(Exception):
    pass


class ClusterJoinError(Exception):
    def __init__(self, cause=None):
        self.cause = cause
        super().__init__(str(cause))
