from fastapi.responses import Response
from fastapi import Request
from aiomysql import DictCursor

from src import Endpoint, Method, Connection, UserType, ResponseType, getResponse

class GetUsers(Endpoint):
    
    async def callback(self, request: Request, format: ResponseType = None) -> Response:
        response = getResponse(format)
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
                            return response({"error": "User is not permitted to view this content."}, 401)
                    return response(await cursor.fetchall())
        return response({"error": "User is not permitted to view this content."}, 401)

def setup() -> GetUsers:
    return GetUsers(Method.GET, "/users")