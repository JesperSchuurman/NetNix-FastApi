import unittest
import requests

class AdminTest(unittest.TestCase):

    def testLoginShouldReturnToken(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/admin/login", data={"email": "senior@mail.test", "password": "senioradminwachtwoord123"})
        self.assertTrue("token" in request.json().keys())

    def testLoginShouldReturn400(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/admin/login", data={"email": "nonexistinguser", "password": "password"})
        self.assertEqual(request.status_code, 400)

    def testLoginShouldReturn401(self) -> None:
        request = requests.post("https://netnix.xyz/api/v1/admin/login", data={"email": "senior@mail.test", "password": "password"})
        self.assertEqual(request.status_code, 401)

if __name__ == "__main__":
    unittest.main()