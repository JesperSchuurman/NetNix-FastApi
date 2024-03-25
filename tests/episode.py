import unittest
import requests

token = requests.post("https://netnix.xyz/api/v1/admin/login", data={"email": "senior@mail.test", "password": "senioradminwachtwoord123"}).json()["token"]
class SerieTest(unittest.TestCase):

    def testEpisodeGetShouldReturnAllEpisodeFromSerie(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/episode/get?serie_id=1", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(1, request.json()[0]["episode_id"])
        self.assertTrue(isinstance(request.json(), list))

    def testEpisodeGetShouldReturnSpecificEpisode(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/episode/get?id=1", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.json()["title"], "Short Action Movie")

    def testEpisodeGetShouldReturn401(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/episode/get")
        self.assertEquals(request.status_code, 401)

    def testEpisodeGetShouldReturn400(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/episode/get?id=129", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.status_code, 400)  
    
    def testEpisodeGetShouldReturn400_2(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/episode/get", headers={"Authorization": f"Bearer {token}"})
        self.assertEquals(request.status_code, 400)  

if __name__ == "__main__":
    unittest.main()