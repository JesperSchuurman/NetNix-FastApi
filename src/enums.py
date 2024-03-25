from enum import Enum

class Method(Enum):
    GET = 0
    POST = 1
    PUT = 2
    DELETE = 3
    PATCH = 4

class UserType(Enum):
    SENIOR = 1
    MEDIOR = 2
    JUNIOR = 3
    DEFAULT = 4