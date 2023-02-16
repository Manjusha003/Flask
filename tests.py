
import unittest
from app import create_app
class TestCase(unittest.TestCase):
    def setUp(self):
        self.post_url = "http://127.0.0.1:5000/register"
        self.get_url = "http://127.0.0.1:5000/students"
        self.app = create_app()
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()



    def test_student_list(self):
        response = self.client.get(self.get_url)
        status = response.status_code
        self.assertEqual(status, 200)

    def test_register(self):
        # data = {"name": "Manjusha", "email": "manju233@gmail.com"}
        data={}
        response = self.client.post(self.post_url, json=data)
        status = response.status_code
        self.assertEqual(status, 200)

    def test_student_by_id(self):
        data = {"name": "Manjusha raut", "email": "manju2336@gmail.com"}
        create_response = self.client.post(self.post_url, json=data)
        item_id = create_response.json["payload"]["_id"]
        url = f"{self.get_url}/{item_id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        self.ctx.pop()
        





