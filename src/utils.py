import aiomysql
import os

from fastapi.responses import Response, JSONResponse
from typing import Any
from dicttoxml import dicttoxml

from .enums import UserType, ResponseType

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_JUNIOR = os.getenv("DB_JUNIOR")
DB_JUNIORPASSWORD = os.getenv("DB_JUNIORPASSWORD")
DB_MEDIOR = os.getenv("DB_MEDIOR")
DB_MEDIORPASSWORD = os.getenv("DB_MEDIORPASSWORD")
DB_SENIOR = os.getenv("DB_SENIOR")
DB_SENIORPASSWORD = os.getenv("DB_SENIORPASSWORD")

class Connection:

    def __init__(self, user: UserType = UserType.DEFAULT) -> None:
        match user:
            case UserType.JUNIOR:
                self.username = DB_JUNIOR
                self.password = DB_JUNIORPASSWORD
            case UserType.MEDIOR:
                self.username = DB_MEDIOR
                self.password = DB_MEDIORPASSWORD
            case UserType.SENIOR:
                self.username = DB_SENIOR
                self.password = DB_SENIORPASSWORD
            case _:
                self.username = DB_USER
                self.password = DB_PASSWORD
        self.connection: aiomysql.Connection = None

    async def __aenter__(self) -> aiomysql.Connection:
        self.connection = await aiomysql.connect("127.0.0.1", self.username, self.password, DB_NAME)
        return self.connection
    
    async def __aexit__(self, *args) -> None:
        self.connection.close()

class Authorization:

    def __init__(self, email: str, usertype: UserType) -> None:
        self.email = email
        self.usertype = usertype

class XMLResponse(Response):

    def __init__(self, content: Any, *args, **kwargs) -> None:
        kwargs.pop("media_type", None)
        kwargs.pop("content", None)
        args = [arg for arg in args if arg not in ["content", "media_type"]]
        super().__init__(dicttoxml(content, False), media_type="text/xml", *args, **kwargs)

def getResponse(responseType: ResponseType) -> type[JSONResponse] | type[XMLResponse]:
    match responseType:
        case ResponseType.XML:
            return XMLResponse
        case _:
            return JSONResponse