from unittest import TestCase

from models.base.document import IndexedDocument, Document
from models.base.field import Field, ReferenceDocumentsField, ReferenceSet
from models.base.meta_document import MetaDocument


class MetaDocumentTest(TestCase):
    def test_multiple_primary_key(self):
        with self.assertRaises(MetaDocument.MultiplePrimaryKeyError):
            class DemoIndexedDocument(IndexedDocument):
                id = Field(primary_key=True)
                name = Field(primary_key=True)


class BasicDocumentTest(TestCase):
    class DemoIndexedDocument(IndexedDocument):
        name = Field(primary_key=True)
        password = Field()
        __private_data = Field()

    def test_create_document(self):
        doc = self.DemoIndexedDocument(name='test', password='test')
        self.assertEqual(doc.name, 'test')
        self.assertEqual(doc.password, 'test')

    def test_compulsory_primary_key(self):
        with self.assertRaises(Document.PrimaryKeyNotSetError):
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


class DocumentReferenceTest(TestCase):
    class DemoDocument(Document):
        name = Field()

    class DemoNestedDocument(IndexedDocument):
        name = Field(primary_key=True)
        children = ReferenceDocumentsField()

    def setUp(self) -> None:
        children = [
            self.DemoDocument(name='a'),
            self.DemoDocument(name='b'),
            self.DemoDocument(name='c')
        ]
        self.document = self.DemoNestedDocument(name='test', children=children)

    def test_retrieval(self):
        self.assertEqual(3, len(self.document.children))

    def test_add(self):
        self.document.children.add(self.DemoDocument(name='d'))
        self.assertEqual(4, len(self.document.children))

    def test_add_incorrect_type(self):
        with self.assertRaises(ReferenceSet.MultipleTypeError):
            self.document.children.add(self.DemoNestedDocument(name='d'))

    def test_remove(self):
        self.document.children.remove(self.DemoDocument(name='a'))
        self.assertFalse(self.DemoDocument(name='a') in self.document.children)

    def test_delete_referee(self):
        referee = next(iter(self.document.children))
        referee.delete()
        self.assertEqual(len(self.document.children), 2)

    def test_find_referee(self):
        children = [
            self.DemoNestedDocument(name='child_1', children=[]),
            self.DemoNestedDocument(name='child_2', children=[]),
            self.DemoNestedDocument(name='child_3', children=[])
        ]
        document = self.DemoNestedDocument(name='test', children=children)
        self.assertEqual(document.children.get('child_1'), children[0])

    def test_delete_referee_by_key(self):
        children = [
            self.DemoNestedDocument(name='child_1', children=[]),
            self.DemoNestedDocument(name='child_2', children=[]),
            self.DemoNestedDocument(name='child_3', children=[])
        ]
        document = self.DemoNestedDocument(name='test', children=children)
        self.assertEqual(document.children.get('child_1'), children[0])
        del document.children['child_1']
        self.assertIsNone(document.children.get('child_1'))

    def test_delete_multiple_references(self):
        referee = self.DemoDocument(name='e')
        document_1 = self.DemoNestedDocument(name='test_1', children=[referee])
        document_2 = self.DemoNestedDocument(name='test_2', children=[referee])
        self.assertTrue(referee in document_1.children)
        self.assertTrue(referee in document_2.children)
        referee.delete()
        self.assertFalse(referee in document_1.children)
        self.assertFalse(referee in document_2.children)

    def test_delete_indexed_document_reference(self):
        referee = self.DemoNestedDocument(name='test_1', children=[])
        document = self.DemoNestedDocument(name='test_2', children=[referee])
        self.assertTrue(referee in document.children)
        referee.delete()
        self.DemoNestedDocument.reload()
        self.assertIsNone(self.DemoNestedDocument.find('test_1'))
        self.assertFalse(referee in document.children)

    def test_delete_deep_reference(self):
        root_referee = self.DemoDocument(name='f')
        mid_referee = self.DemoNestedDocument(name='test_1', children=[root_referee])
        document = self.DemoNestedDocument(name='test_2', children=[mid_referee])
        root_referee.delete()
        self.DemoNestedDocument.reload()
        for referee in document.children:
            self.assertFalse(root_referee in referee.children)

    def test_typed_reference_field(self):
        """
        Test that type checking is enforced when defining ReferenceDocumentsField with a specific data_type.
        """

        class DemoTypedNestedDocument(Document):
            name = Field(primary_key=True)
            children = ReferenceDocumentsField(data_type=self.DemoDocument)

        # This should not raise an exception
        DemoTypedNestedDocument(name='test', children=[self.DemoDocument(name='a')])
        with self.assertRaises(ReferenceSet.MultipleTypeError):
            DemoTypedNestedDocument(name='test', children=[self.DemoNestedDocument(name='a')])

    def test_find_referred_by(self):
        referee = self.DemoDocument(name='e')
        referrer = self.DemoNestedDocument(name='test_1', children=[referee])
        self.assertEqual(referee.find_referred_by(referrer_type=self.DemoNestedDocument, field_name='children'),
                         referrer)
        referrer.children.remove(referee)
        with self.assertRaises(Document.ReferrerNotFound):
            referee.find_referred_by(referrer_type=self.DemoNestedDocument, field_name='children')

    def tearDown(self) -> None:
        self.DemoNestedDocument.delete_all()
