from fastapi.responses import Response
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class PatchEpisode(Endpoint):

    async def callback(self, format: ResponseType = None, title: str = Form(None), duration: int = Form(None), serieId: int = Form(), season: int = Form(None), filepath: str = Form(None), id: int = Form()) -> Response:
        response = getResponse(format)
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                await cursor.execute("SELECT * FROM Serie WHERE id = %s", (serieId,))
                if await cursor.fetchone():
                    return response({"error": "This serie does not exist."})
                else:
                    await cursor.execute("SELECT * FROM Episode WHERE id = %s", (id,))
                    result = await cursor.fetchone()
                    if not result:
                        return response({"error": "This episode does not exist."})
                    if not title:
                        title = result[1]
                    if not duration:
                        duration = result[2]
                    if not season:
                        season = result[4]
                    if not filepath:
                        filepath = result[5]
                    await cursor.callproc("update_movie", (id, title, duration, serieId, season, filepath))
                    await db.commit()
                    return response({})

def setup() -> PatchEpisode:
    return PatchEpisode(Method.PATCH, "/movie/post")