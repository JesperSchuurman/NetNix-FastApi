import unittest
import requests

token = requests.post("https://netnix.xyz/api/v1/admin/login", data={"email": "senior@mail.test", "password": "senioradminwachtwoord123"}).json()["token"]
class SerieTest(unittest.TestCase):

    def testSerieGetShouldReturnAllSeries(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/serie/get", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(1, request.json()[0]["id"])
        self.assertTrue(isinstance(request.json(), list))

    def testSerieGetShouldReturnSpecificSerie(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/serie/get?id=1", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.json()["title"], "oneSeasonActionSerie")

    def testSerieGetShouldReturn401(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/serie/get")
        self.assertEquals(request.status_code, 401)

    def testSerieGetShouldReturn400(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/serie/get?id=129", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.status_code, 400) 

    def testSerieShouldPostNewSerieToDatabase(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/serie/get?id=3", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.status_code, 400)
        requests.post("https://netnix.xyz/api/v1/serie/post", data={"title": "threeSeasonActionSerie", "genreId": 1, "resolution": "HD"})
        request = requests.get("https://netnix.xyz/api/v1/serie/get?id=3", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.json()["title"], "threeSeasonActionSerie")

    def testSerieShouldReturn400_2(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/serie/post", data={"title": "threeSeasonActionSerie", "resolution": "HD"})
        self.assertEquals(request.status_code, 400)

    def testSerieShouldReturn400_3(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/serie/post", data={"title": "oneSeasonActionSerie", "genreId": 1, "resolution": "HD"})
        self.assertEquals(request.status_code, 400)

if __name__ == "__main__":
    unittest.main()