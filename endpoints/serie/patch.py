from fastapi.responses import Response
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class PatchSerie(Endpoint):

    async def callback(self, format: ResponseType = None, title: str = Form(), genreId: int = Form(), resolution: str = Form(), id: int = Form()) -> Response:
        response = getResponse(format)
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
                    return response({})
                else:
                    return response({"error": "There is no serie selected."}, 400)

def setup() -> PatchSerie:
    return PatchSerie(Method.PATCH, "/serie/post", Response)