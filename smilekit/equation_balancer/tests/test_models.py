from django.test import TestCase
from smilekit.equation_balancer.models import Module


class TestModule(TestCase):
    def test_unicode(self):
        m = Module(name="foo")
        self.assertEqual(str(m), "foo")

    def test_dir(self):
        m = Module(name="foo")
        self.assertEqual(m.dir, dir(m))
