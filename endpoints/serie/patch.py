from fastapi.responses import Response
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class PatchSerie(Endpoint):

    async def callback(self, format: ResponseType = None, title: str = Form(None), genreId: int = Form(None), resolution: str = Form(None), id: int = Form()) -> Response:
        response = getResponse(format)
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                await cursor.execute("SELECT * FROM Serie WHERE id = %s", (id,))
                result = await cursor.fetchone()
                if not result:
                    return response({"error": "There is no serie selected."}, 400)
                if not title:
                    title = result[0]
                if not genreId:
                    genreId = result[1]
                if not resolution:
                    resolution = result[2]
                await cursor.callproc("update_serie", (id, title, genreId, resolution))
                await db.commit()
                return response({})

def setup() -> PatchSerie:
    return PatchSerie(Method.PATCH, "/serie/post")