from airss_downloader.models import \
    Contents, \
    Sources
from tests.factories import \
    ContentsFactory, \
    SourcesFactory

import pytest


class BaseModelTest:
    """
    Abstract base test class to refactor model tests.

    The Children classes must define the following attributes:
        self.model: The model object to test.
        self.dummy_instance: A factory object of the model to test.
        self.model_attributes: List of model attributes to test

    Public attributes:
        dummy_instance (Factory_boy object): Dummy instance of the model.
    """

    @pytest.fixture(autouse=True)
    def base_setup(self, session):
        self.session = session

    def test_attributes_defined(self):
        for attribute in self.model_attributes:
            assert getattr(self.model, attribute) == \
                getattr(self.dummy_instance, attribute)


@pytest.mark.usefixtures('base_setup')
class TestSources(BaseModelTest):

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.factory = SourcesFactory
        self.dummy_instance = SourcesFactory.create()
        self.model = Sources(
            id=self.dummy_instance.id,
            title=self.dummy_instance.title,
            description=self.dummy_instance.description,
            created_date=self.dummy_instance.created_date,
            published_date=self.dummy_instance.published_date,
            updated_date=self.dummy_instance.updated_date,
            url=self.dummy_instance.url,
        )
        self.model_attributes = [
            'id',
            'title',
            'description',
            'created_date',
            'published_date',
            'updated_date',
            'url',
        ]


@pytest.mark.usefixtures('base_setup')
class TestContents(BaseModelTest):

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.factory = ContentsFactory
        self.dummy_instance = ContentsFactory.create()
        self.model = Contents(
            id=self.dummy_instance.id,
            title=self.dummy_instance.title,
            created_date=self.dummy_instance.created_date,
            published_date=self.dummy_instance.published_date,
            updated_date=self.dummy_instance.updated_date,
            url=self.dummy_instance.url,
            author_id=self.dummy_instance.author_id,
        )
        self.model_attributes = [
            'id',
            'title',
            'created_date',
            'published_date',
            'updated_date',
            'url',
            'author_id',
        ]
