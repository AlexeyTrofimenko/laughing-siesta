from django.db.utils import IntegrityError
from django.test import TestCase

from web.models import Topic


class TopicModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Topic.objects.create(name="T1", desc="D1")

    def test_name_max_length(self):
        t = Topic.objects.get(id=1)
        max_length = t._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_name_unique(self):
        with self.assertRaises(IntegrityError):
            Topic.objects.create(name="T1", desc="D2")

    def test_desc_max_length(self):
        t = Topic.objects.get(id=1)
        max_length = t._meta.get_field('desc').max_length
        self.assertEquals(max_length, 5000)

    def test_desc_blank(self):
        Topic.objects.create(name="T2")
        t = Topic.objects.get(id=2)
        self.assertIsInstance(t.desc, str)

    def test_object_name_is_name(self):
        t = Topic.objects.get(id=1)
        expected_object_name = t.name
        self.assertEquals(expected_object_name, str(t))
