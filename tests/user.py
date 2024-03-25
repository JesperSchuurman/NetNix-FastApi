import unittest
import requests
import random

ADMIN_AUTH = {"Authorization": "Bearer " + requests.post("https://netnix.xyz/api/v1/admin/login", data={"email": "senior@mail.test", "password": "senioradminwachtwoord123"}).json()["token"]}
USER_AUTH = {"Authorization": "Bearer " + requests.post("https://netnix.xyz/api/v1/user/login", data={"email": "sdAccount@mail.test", "password": "1@drieVierVIJF"}).json()["token"]}

class UserTest(unittest.TestCase):

    def testLoginShouldReturnToken(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/login", data={"email": "sdAccount@mail.test", "password": "1@drieVierVIJF"})
        self.assertTrue("token" in request.json().keys())

    def testLoginShouldReturn400(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/login", data={"email": "nonexistinguser", "password": "password"})
        self.assertEqual(request.status_code, 400)

    def testLoginShouldReturn401(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/login", data={"email": "sdAccount@mail.test", "password": "password"})
        self.assertEqual(request.status_code, 401)

    def testRegisterShouldSucceed(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/register", data={"email": f"newuser{random.randint(0,1000000000)}(@mail.test", "password": "StrongPassword"})
        self.assertEqual(request.status_code, 200)

    def testRegisterShouldReturn400(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/user/register", data={"email": "sdAccount@mail.test", "password": "StrongPassword"})
        self.assertEqual(request.status_code, 400)

    def testGetMonthlyProfitsShouldReturn4096(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/user/getMonthlyProfits", headers=ADMIN_AUTH)
        self.assertEqual(request.json()["profit"], 40.96)

    def testGetMonthlyProfitsShouldReturn401(self) -> None:
        request = requests.get("https://netnix.xyz/api/v1/user/getMonthlyProfits", headers=USER_AUTH)
        self.assertEqual(request.status_code, 401)

if __name__ == "__main__":
    unittest.main()