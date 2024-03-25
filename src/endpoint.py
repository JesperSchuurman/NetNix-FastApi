import datetime
import os

from typing import Any
from fastapi.responses import Response
from passlib.context import CryptContext
from jose import jwt

from . import Method
from .utils import Connection, Authorization
from .enums import UserType

SIGNING_KEY = os.getenv("SIGNING_KEY")

class Endpoint:

    def __init__(self, method: Method, path: str, responseClass: Response) -> None:
        self.jwt = CryptContext(["bcrypt"])
        self.method = method
        self.path = path
        self.responseClass = responseClass

    async def callback(self) -> Any:
        raise NotImplementedError
    
    async def getAuthorization(self, token: str | None, admin: bool = False) -> Authorization | None:
        if token and token.startswith("Bearer "):
            data = jwt.decode(token.split("Bearer ", 1)[1], SIGNING_KEY)
            if data["exp"].isdigit() and datetime.datetime.fromtimestamp(int(data["exp"])) > datetime.datetime.utcnow():
                async with Connection() as db:
                    async with db.cursor() as cursor:
                        if admin:
                            await cursor.execute("SELECT role FROM Admin WHERE email = %s", (data["sub"],))
                            result = await cursor.fetchone()
                            if result:
                                return Authorization(data["sub"], UserType(result[0]))
                        else:
                            await cursor.execute("SELECT email FROM Account WHERE email = %s", (data["sub"],))
                            if await cursor.fetchone():
                                return Authorization(data["sub"], UserType.DEFAULT)