from fastapi.responses import Response
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class PostMovie(Endpoint):

    async def callback(self, format: ResponseType = None, title: str = Form(), duration: int = Form(), genreId: int = Form(), filepath: str = Form(), resolution: str = Form()) -> Response:
        response = getResponse(format)
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                if title and duration and genreId and filepath and resolution:
                    await cursor.execute("SELECT * FROM Movie WHERE title = %s", (title,))
                    if await cursor.fetchone():
                        return response({"error": "This movie already exists."}, 400)
                    else:
                        await cursor.callproc("add_movie", (title, duration, genreId, filepath, resolution))
                        await db.comit()
                        return response({})
                else:
                    return response({"error": "Not all fields are filled in."}, 400)

def setup() -> PostMovie:
    return PostMovie(Method.POST, "/movie/post")