from unittest import TestCase

from models.base.document import IndexedDocument, Document
from models.base.field import Field, ReferenceDocumentSetField


class MetaDocumentTest(TestCase):
    def test_multiple_primary_key(self):
        with self.assertRaises(Field.MultiplePrimaryKeyError):
            class DemoIndexedDocument(IndexedDocument):
                id = Field(primary_key=True)
                name = Field(primary_key=True)


class BasicDocumentTest(TestCase):
    class DemoIndexedDocument(IndexedDocument):
        name = Field(primary_key=True)
        password = Field()

    def test_create_document(self):
        doc = self.DemoIndexedDocument(name='test', password='test')
        self.assertEqual(doc.name, 'test')
        self.assertEqual(doc.password, 'test')

    def test_compulsory_primary_key(self):
        with self.assertRaises(Field.PrimaryKeyNotSetError):
            self.DemoIndexedDocument(password='test')


class DocumentPersistenceTest(TestCase):
    class DemoIndexedDocument(IndexedDocument):
        id = Field(primary_key=True)
        name = Field()

    def setUp(self) -> None:
        self.DemoIndexedDocument(id=1, name='a')
        self.DemoIndexedDocument(id=2, name='b')
        self.DemoIndexedDocument(id=3, name='c')

    def test_persistence(self):
        self.DemoIndexedDocument.reload()
        self.assertEqual(len(self.DemoIndexedDocument.all()), 3)

    def test_find(self):
        document = self.DemoIndexedDocument.find(1)
        self.assertEqual(document.name, 'a')
        document = self.DemoIndexedDocument.find(10)
        self.assertIsNone(document)

    def test_delete(self):
        self.DemoIndexedDocument(id=4, name='d')
        document = self.DemoIndexedDocument.find(4)
        self.assertIsNotNone(document)
        document.delete()
        self.DemoIndexedDocument.reload()
        document = self.DemoIndexedDocument.find(4)
        self.assertIsNone(document)

    def tearDown(self) -> None:
        self.DemoIndexedDocument.delete_all()


class EmbeddedDocumentTest(TestCase):
    class DemoEmbeddedDocument(Document):
        name = Field()

    class DemoNestedDocument(IndexedDocument):
        name = Field(primary_key=True)
        children = ReferenceDocumentSetField()

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

    def test_delete_referee(self):
        referee = next(iter(self.document.children))
        referee.delete()
        self.assertEqual(len(self.document.children), 2)

    # TODO: test delete multiple references
    # TODO: test delete Document with referrer
    # TODO: test delete deeply nested Document

    def tearDown(self) -> None:
        self.DemoNestedDocument.delete_all()
