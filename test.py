from rest_framework.test import APITestCase
import json


class BaseTestCase(APITestCase):
    def get_api(self, url):
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        self.assertEqual(data['success'], True)
        return data.get('data', None)

    def get_api_fail(self, url):
        res = self.client.get(url)
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.content)
        self.assertEqual(data['success'], False)
        return data.get('data', None)

    def post_api(self, url, data=None):
        res = self.client.post(url, data, format='json')
        if res.status_code != 200:
            print(res.content)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.content)
        if data['success'] is False:
            print(data)
        self.assertEqual(data['success'], True)
        return data.get('data', None)

    def post_api_fail(self, url, data=None):
        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.content)
        self.assertEqual(data['success'], False)
        return data.get('data', None)
