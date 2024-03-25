class MissingSetupFunction(RuntimeError):
    
    def __init__(self) -> None:
        super().__init__("The endpoint provided does not contain a setup function")

class DatabaseNotConnected(RuntimeError):

    def __init__(self) -> None:
        super().__init__("No database connected.")