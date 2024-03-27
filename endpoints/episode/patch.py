from fastapi.responses import Response
from fastapi import Form
from aiomysql.cursors import DictCursor

from src import Endpoint, Method, Connection, ResponseType, getResponse

class PatchEpisode(Endpoint):

    async def callback(self, format: ResponseType = None, title: str = Form(), duration: int = Form(), serieId: int = Form(), season: int = Form(), filepath: str = Form(), id: int = Form()) -> Response:
        response = getResponse(format)
        async with Connection() as db:
            async with db.cursor(DictCursor) as cursor:
                if id:
                    await cursor.execute("SELECT * FROM Serie WHERE id = %s", (serieId,))
                    if await cursor.fetchone():
                        return response({"error": "This serie does not exist."})
                    else:
                        await cursor.execute("SELECT * FROM Episode WHERE id = %s", (id,))
                        result = await cursor.fetchone()
                        if not title:
                            title = result.title()
                        if not duration:
                            duration = result.duration()
                        if not serieId:
                            serieId = result.serie_id()
                        if not season:
                            season = result.resoltuion()
                        if not filepath:
                            filepath = result.filepath()
                        await cursor.callproc("update_movie", (id, title, duration, serieId, season, filepath))
                        await db.comit()
                        return response({})
                else:
                    return response({"error": "There is no movie selected."}, 400)

def setup() -> PatchEpisode:
    return PatchEpisode(Method.PATCH, "/movie/post")