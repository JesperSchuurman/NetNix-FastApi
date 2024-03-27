from fastapi.responses import Response
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class PatchMovie(Endpoint):

    async def callback(self, format: ResponseType = None, title: str = Form(None), duration: str = Form(None), genreId: int = Form(None), filepath: str = Form(None), resolution: str = Form(None), id: int = Form()) -> Response:
        response = getResponse(format)
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                await cursor.execute("SELECT * FROM Movie WHERE id = %s", (id,))
                result = await cursor.fetchone()
                if not result:
                    return response({"error": "Movie does not exist."}, 400)
                if not title:
                    title = result[1]
                if not duration:
                    duration = result[2]
                if not genreId:
                    genreId = result[3]
                if not filepath:
                    filepath = result[4]
                if not resolution:
                    resolution = result[5]
                await cursor.callproc("update_movie", (id, title, duration, genreId, filepath, resolution))
                await db.commit()
                return response({})

def setup() -> PatchMovie:
    return PatchMovie(Method.PATCH, "/movie/post")