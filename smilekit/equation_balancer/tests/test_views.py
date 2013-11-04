from django.test import TestCase, Client


class TestRecalculate(TestCase):
    def setUp(self):
        self.c = Client()

    def test_recalculate(self):
        r = self.c.post('/weights/recalculate/', dict())
        self.assertEqual(r.status_code, 302)
