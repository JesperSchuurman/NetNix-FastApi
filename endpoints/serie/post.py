from fastapi.responses import JSONResponse
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection

class PostSerie(Endpoint):

    async def callback(self, title: str = Form(), genreId: int = Form(), resolution: str = Form()) -> JSONResponse:
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                if title and genreId and resolution:
                    await cursor.execute("SELECT * FROM Serie WHERE title = %s", (title,))
                    if await cursor.fetchone():
                        return JSONResponse({"error": "This serie already exists."}, 400)
                    else:
                        await cursor.callproc("add_serie", (title, genreId, resolution))
                        await db.comit()
                        return JSONResponse({})
                else:
                    return JSONResponse({"error": "Not all fields are filled in."}, 400)

def setup() -> PostSerie:
    return PostSerie(Method.POST, "/serie/post", JSONResponse)