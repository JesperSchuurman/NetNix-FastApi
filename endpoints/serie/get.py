from fastapi.responses import JSONResponse
from fastapi import Request
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection

class GetSerie(Endpoint):

    async def callback(self, request: Request, id: int | None = None) -> JSONResponse:
        if auth := await self.getAuthorization(request.headers.get("Authorization", None), True):
            async with Connection(auth.usertype) as db:
                async with db.cursor(DictCursor) as cursor:
                    if id:
                        await cursor.execute("SELECT * FROM Serie WHERE id = %s", (id,))
                        result = await cursor.fetchone()
                        if not result:
                            return JSONResponse({"error": "This serie does not exist."}, 400)
                    else:
                        await cursor.callproc("get_series")
                        result = await cursor.fetchall()
                        if not result:
                            return JSONResponse({"error": "No series found."}, 400)
                    return JSONResponse(result)
        return JSONResponse({"error": "User is not permitted to view this content."}, 401)
            
def setup() -> GetSerie:
    return GetSerie(Method.GET, "/serie/get", JSONResponse)