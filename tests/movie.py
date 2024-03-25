import unittest
import requests

token = requests.post("https://netnix.xyz/api/v1/admin/login", data={"email": "senior@mail.test", "password": "senioradminwachtwoord123"}).json()["token"]
class MovieTest(unittest.TestCase):

    def testMovieGetShouldReturnAllMovies(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/movie/get", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(1, request.json()[0]["id"])
        self.assertTrue(isinstance(request.json(), list))

    def testMovieGetShouldReturnSpecificMovie(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/movie/get?id=1", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.json()["title"], "Short Action Movie")

    def testMovieGetShouldReturn401(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/movie/get")
        self.assertEquals(request.status_code, 401)

    def testMovieGetShouldReturn400(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/movie/get?id=129", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.status_code, 400)  

if __name__ == "__main__":
    unittest.main()