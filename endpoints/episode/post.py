from fastapi.responses import Response
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class PostEpisode(Endpoint):

    async def callback(self, format: ResponseType = None, title: str = Form(), duration: int = Form(), serieId: int = Form(), season: int = Form(), filepath: str = Form()) -> Response:
        response = getResponse(format)
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                if title and duration and serieId and season and filepath:
                    await cursor.execute("SELECT * FROM Episode WHERE title = %s", (title,))
                    if await cursor.fetchone():
                        return response({"error": "This episode already exists."}, 400)
                    await cursor.execute("Select * FROM Serie WHERE id = %s", (serieId,))
                    if await cursor.fetchone():
                        return response({"error": "This serie doesn't exist."}, 400)
                    else:
                        await cursor.callproc("add_episode", (title, duration, serieId, season, filepath))
                        await db.comit()
                        return response({})
                else:
                    return response({"error": "Not all fields are filled in."}, 400)

def setup() -> PostEpisode:
    return PostEpisode(Method.POST, "/episode/post")