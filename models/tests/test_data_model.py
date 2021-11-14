from unittest import TestCase

from models.data_model import Document, EmbeddedDocument


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


class EmbeddedDocumentTest(TestCase):
    class DemoEmbeddedDocument(EmbeddedDocument):
        def __init__(self, name):
            self.name = name

    class DemoNestedDocument(Document):
        def __init__(self, key, children):
            self.children = children

            super().__init__(key)

    def setUp(self) -> None:
        children = [
            self.DemoEmbeddedDocument(name='a'),
            self.DemoEmbeddedDocument(name='b'),
            self.DemoEmbeddedDocument(name='c')
        ]
        self.DemoNestedDocument(key=1, children=children)

    def tearDown(self) -> None:
        self.DemoNestedDocument.delete_all()
