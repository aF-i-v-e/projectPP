import unittest
from src.main import app
from datetime import datetime

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello World at', response.data)

    def test_response_time(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        current_time = datetime.now().strftime('%H:%M:%S')
        expected_message = f'<b>Hello World at {current_time}</b>!'
        response_data = response.data.decode('utf-8')
        self.assertEqual(expected_message, response_data)

if __name__ == '__main__':
    unittest.main()
