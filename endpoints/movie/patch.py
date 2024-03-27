from fastapi.responses import JSONResponse
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection

class PatchMovie(Endpoint):

    async def callback(self, title: str = Form(), duration: str = Form(), genreId: int = Form(), filepath: str = Form(), resolution: str = Form(), id: int = Form()) -> JSONResponse:
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                if id:
                    await cursor.execute("SELECT * FROM Movie WHERE id = %s", (id,))
                    result = await cursor.fetchone()
                    if not title:
                        title = result.title()
                    if not duration:
                        duration = result.duration()
                    if not genreId:
                        genreId = result.genre_id()
                    if not filepath:
                        filepath = result.filepath()
                    if not resolution:
                        resolution = result.resoltuion()
                    await cursor.callproc("update_movie", (id, title, duration, genreId, filepath, resolution))
                    await db.comit()
                    return JSONResponse({})
                else:
                    return JSONResponse({"error": "There is no movie selected."}, 400)

def setup() -> PatchMovie:
    return PatchMovie(Method.PATCH, "/movie/post", JSONResponse)