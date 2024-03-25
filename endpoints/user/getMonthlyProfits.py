from fastapi import Request
from fastapi.responses import JSONResponse

from src import Endpoint, Method, Connection, UserType

class GetMonthlyProfits(Endpoint):

    async def callback(self, request: Request) -> JSONResponse:
        if auth := await self.getAuthorization(request.headers.get("Authorization", None), True):
            async with Connection(UserType(auth.usertype)) as db:
                async with db.cursor() as cursor:
                    await cursor.callproc("get_subscription_data")
                    results = await cursor.fetchall()
            if not results:
                return JSONResponse({"error": "No subscriptions found."}, 400)
            profits = 0.0
            for result in results:
                profits += result[3]
            return JSONResponse({"profit": profits})
        return JSONResponse({"error": "User is not permitted to view this content."}, 401)
            
def setup() -> GetMonthlyProfits:
    return GetMonthlyProfits(Method.GET, "/user/getMonthlyProfits", JSONResponse)