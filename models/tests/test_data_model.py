from unittest import TestCase

from models.data_model import Document


class DocumentTest(TestCase):
    class DemoDocument(Document):
        pass

    def test_persistence(self):
        self.DemoDocument(key=1)
        self.DemoDocument(key=2)
        self.DemoDocument(key=3)
        self.DemoDocument.reload()
        self.assertEqual(len(self.DemoDocument.all()), 3)

    def tearDown(self) -> None:
        self.DemoDocument.delete_all()
