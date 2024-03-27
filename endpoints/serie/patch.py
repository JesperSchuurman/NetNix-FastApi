from fastapi.responses import JSONResponse
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection

class PatchSerie(Endpoint):

    async def callback(self, title: str = Form(), genreId: int = Form(), resolution: str = Form(), id: int = Form()) -> JSONResponse:
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                if id:
                    await cursor.execute("SELECT * FROM Serie WHERE id = %s", (id,))
                    result = await cursor.fetchone()
                    if not title:
                        title = result.title()
                    if not genreId:
                        genreId = result.genre_id()
                    if not resolution:
                        resolution = result.resoltuion()
                    await cursor.callproc("update_serie", (id, title, genreId, resolution))
                    await db.comit()
                    return JSONResponse({})
                else:
                    return JSONResponse({"error": "There is no serie selected."}, 400)

def setup() -> PatchSerie:
    return PatchSerie(Method.PATCH, "/serie/post", JSONResponse)