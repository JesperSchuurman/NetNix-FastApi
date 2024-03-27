from fastapi.responses import Response
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class PostSerie(Endpoint):

    async def callback(self, format: ResponseType = None, title: str = Form(), genreId: int = Form(), resolution: str = Form()) -> Response:
        response = getResponse(format)
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                if title and genreId and resolution:
                    await cursor.execute("SELECT * FROM Serie WHERE title = %s", (title,))
                    if await cursor.fetchone():
                        return response({"error": "This serie already exists."}, 400)
                    else:
                        await cursor.callproc("add_serie", (title, genreId, resolution))
                        await db.comit()
                        return response({})
                else:
                    return response({"error": "Not all fields are filled in."}, 400)

def setup() -> PostSerie:
    return PostSerie(Method.POST, "/serie/post")