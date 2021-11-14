from unittest import TestCase

from models.data_model import Document


class DocumentTest(TestCase):
    class DemoDocument(Document):
        def __init__(self, key, name):
            self.name = name
            super().__init__(key)

    def setUp(self) -> None:
        self.DemoDocument(key=1, name='a')
        self.DemoDocument(key=2, name='b')
        self.DemoDocument(key=3, name='c')

    def test_persistence(self):
        self.DemoDocument.reload()
        self.assertEqual(len(self.DemoDocument.all()), 3)

    def test_find(self):
        document = self.DemoDocument.find(1)
        self.assertEqual(document.name, 'a')
        document = self.DemoDocument.find(10)
        self.assertIsNone(document)

    def test_delete(self):
        self.DemoDocument(key=4, name='d')
        document = self.DemoDocument.find(4)
        self.assertIsNotNone(document)
        document.delete()
        self.DemoDocument.reload()
        document = self.DemoDocument.find(4)
        self.assertIsNone(document)

    def tearDown(self) -> None:
        self.DemoDocument.delete_all()
