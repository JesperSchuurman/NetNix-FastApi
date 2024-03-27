from fastapi.responses import Response
from fastapi import Request
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class GetMovie(Endpoint):

    async def callback(self, request: Request, format: ResponseType = None, serie_id : int | None = None, id: int | None = None) -> Response:
        response = getResponse(format)
        if auth := await self.getAuthorization(request.headers.get("Authorization", None), True):
            if not serie_id and not id:
                response({"error": "ID and Serie_ID can't both be none"}, 400)
            async with Connection(auth.usertype) as db:
                async with db.cursor(DictCursor) as cursor:
                    if id:
                        await cursor.execute("SELECT * FROM Movie WHERE id = %s", (id,))
                        result = await cursor.fetchone()
                        if not result:
                            return response({"error": "This movie does not exist."}, 400)
                    else:
                        await cursor.callproc("get_episodes_from_serie", (serie_id,))
                        result = await cursor.fetchall()
                        if not result:
                            return response({"error": "No episodes found or serie does not exist."}, 400)
                    return response(result)
        return response({"error": "User is not permitted to view this content."}, 401)
            
def setup() -> GetMovie:
    return GetMovie(Method.GET, "/episode/get")