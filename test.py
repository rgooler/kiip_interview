#!bin/python
import requests
import unittest


class TestKiip(unittest.TestCase):

    def test_help(self):
        u = 'http://127.0.0.1:5000'
        r = requests.get(u)
        self.assertEqual(r.status_code, 200)

    def test_missing_json(self):
        u = 'http://127.0.0.1:5000'
        r = requests.post(u, json={})
        self.assertEqual(r.status_code, 400)

    def test_web1(self):
        json_blob = {"ip_address": "10.240.0.34", "role": "web"}
        u = 'http://127.0.0.1:5000'
        r = requests.post(u, json=json_blob)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text, "web1")

    def test_bad_ip(self):
        json_blob = {"ip_address": "10.2400.34", "role": "web"}
        u = 'http://127.0.0.1:5000'
        r = requests.post(u, json=json_blob)
        self.assertEqual(r.status_code, 400)

    def test_bad_role(self):
        json_blob = {"ip_address": "10.240.0.34", "role": "afsw"}
        u = 'http://127.0.0.1:5000'
        r = requests.post(u, json=json_blob)
        self.assertEqual(r.status_code, 400)

if __name__ == '__main__':
    unittest.main()
