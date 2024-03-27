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

    def testMovieShouldPostNewMovieToDatabase(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/movie/get?id=4", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.status_code, 400)
        requests.post("https://netnix.xyz/api/v1/movie/post", data={"title": "kung fu panda 2", "duration": 1234, "genreId": 1, "filepath": "movie/kung_fu_panda_2.mp4", "resolution": "UHD"})
        request = requests.get("https://netnix.xyz/api/v1/movie/get?id=4", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.json()["title"], "kung fu panda 2")

    def testMovieShouldReturn400_2(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/movie/post", data={"title": "kung fu panda 3", "resolution": "HD"})
        self.assertEquals(request.status_code, 400)

    def testMovieShouldReturn400_3(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/movie/post", data={"title": "Short Action Movie", "duration": 2715, "genreId": 1, "filepath": "movie1.mp4", "resolution": "SD"})
        self.assertEquals(request.status_code, 400)

if __name__ == "__main__":
    unittest.main()