from fastapi import Request
from fastapi.responses import Response

from src import Endpoint, Method, Connection, UserType, ResponseType, getResponse

class GetMonthlyProfits(Endpoint):

    async def callback(self, request: Request, format: ResponseType = None) -> Response:
        response = getResponse(format)
        if auth := await self.getAuthorization(request.headers.get("Authorization", None), True):
            async with Connection(UserType(auth.usertype)) as db:
                async with db.cursor() as cursor:
                    await cursor.callproc("get_subscription_data")
                    results = await cursor.fetchall()
            if not results:
                return response({"error": "There are not any subscriptions currentley."}, 400)
            profits = 0.0
            for result in results:
                profits += result[3]
            return response({"profit": profits})
        return response({"error": "User is not permitted to view this content."}, 401)
            
def setup() -> GetMonthlyProfits:
    return GetMonthlyProfits(Method.GET, "/user/getMonthlyProfits")