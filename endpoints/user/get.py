from fastapi.responses import JSONResponse
from fastapi import Request
from aiomysql import DictCursor

from src import Endpoint, Method, Connection, UserType

class GetUsers(Endpoint):
    
    async def callback(self, request: Request) -> JSONResponse:
        if auth := await self.getAuthorization(request.headers.get("Authorization", None), True):
            async with Connection(auth.usertype) as db:
                async with db.cursor(DictCursor) as cursor:
                    match auth.usertype:
                        case UserType.JUNIOR:
                            await cursor.callproc("get_accounts_junior")
                        case UserType.MEDIOR:
                            await cursor.callproc("get_accounts_medior")
                        case UserType.SENIOR:
                            await cursor.callproc("get_accounts_senior")
                        case _:
                            return JSONResponse({"error": "User is not permitted to view this content."}, 401)
                    return JSONResponse(await cursor.fetchall())
        return JSONResponse({"error": "User is not permitted to view this content."}, 401)

def setup() -> GetUsers:
    return GetUsers(Method.GET, "/users", JSONResponse)