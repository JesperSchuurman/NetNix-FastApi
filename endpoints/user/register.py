from fastapi.responses import Response
from fastapi import Form

from src import Endpoint, Method, Connection, ResponseType, getResponse

class RegisterUser(Endpoint):
    
    async def callback(self, format: ResponseType = None, email: str = Form(), password: str = Form(), referrer: int | None = Form(None)) -> Response:
        response = getResponse(format)
        async with Connection() as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT email FROM Account WHERE email = %s", (email,))
                if await cursor.fetchone():
                    return response({"error": "User with this email already exists."}, 400)
                await cursor.callproc("add_account", (email, self.jwt.hash(password), None, None, None))
                await db.commit()
                return response({})

def setup() -> RegisterUser:
    return RegisterUser(Method.POST, "/user/register")