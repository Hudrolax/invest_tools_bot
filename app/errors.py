class BackendError(Exception):
    def __init__(self, message: str = "", status: int = 500) -> None:
        self.message = message
        self.status = status
        super().__init__(self.message)


class ConnectionError(Exception):
    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(self.message)


class ClientError(Exception):
    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__(self.message)