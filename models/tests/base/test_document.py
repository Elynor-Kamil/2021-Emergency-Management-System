from unittest import TestCase

from models.base.document import Document, EmbeddedDocument
from models.base.field import Field, ReferenceDocumentSetField


class MetaDocumentTest(TestCase):
    def test_multiple_primary_key(self):
        with self.assertRaises(Field.MultiplePrimaryKeyError):
            class DemoDocument(Document):
                id = Field(primary_key=True)
                name = Field(primary_key=True)


class BasicDocumentTest(TestCase):
    class DemoDocument(Document):
        name = Field(primary_key=True)
        password = Field()

    def test_create_document(self):
        doc = self.DemoDocument(name='test', password='test')
        self.assertEqual(doc.name, 'test')
        self.assertEqual(doc.password, 'test')

    def test_compulsory_primary_key(self):
        with self.assertRaises(Field.PrimaryKeyNotSetError):
            self.DemoDocument(password='test')


class DocumentPersistenceTest(TestCase):
    class DemoDocument(Document):
        id = Field(primary_key=True)
        name = Field()

    def setUp(self) -> None:
        self.DemoDocument(id=1, name='a')
        self.DemoDocument(id=2, name='b')
        self.DemoDocument(id=3, name='c')

    def test_persistence(self):
        self.DemoDocument.reload()
        self.assertEqual(len(self.DemoDocument.all()), 3)

    def test_find(self):
        document = self.DemoDocument.find(1)
        self.assertEqual(document.name, 'a')
        document = self.DemoDocument.find(10)
        self.assertIsNone(document)

    def test_delete(self):
        self.DemoDocument(id=4, name='d')
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
        name = Field()

    class DemoNestedDocument(Document):
        name = Field(primary_key=True)
        children = ReferenceDocumentSetField()  # TODO: reference field list class

    def setUp(self) -> None:
        children = [
            self.DemoEmbeddedDocument(name='a'),
            self.DemoEmbeddedDocument(name='b'),
            self.DemoEmbeddedDocument(name='c')
        ]
        self.document = self.DemoNestedDocument(name='test', children=children)

    def test_retrieval(self):
        self.assertEqual(3, len(self.document.children))

    def test_add(self):
        self.document.children.add(self.DemoEmbeddedDocument(name='d'))
        self.assertEqual(4, len(self.document.children))

    def test_remove(self):
        self.document.children.remove(self.DemoEmbeddedDocument(name='a'))
        self.assertFalse(self.DemoEmbeddedDocument(name='a') in self.document.children)

    def tearDown(self) -> None:
        self.DemoNestedDocument.delete_all()
