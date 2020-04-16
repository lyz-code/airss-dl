from airss_downloader import models
from tests import factories

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
class TestAuthor(BaseModelTest):

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.factory = factories.AuthorFactory
        self.dummy_instance = self.factory.create()
        self.model = models.Author(
            id=self.dummy_instance.id,
            name=self.dummy_instance.name,
        )
        self.model_attributes = [
            'id',
            'name',
        ]


@pytest.mark.usefixtures('base_setup')
class TestCategory(BaseModelTest):

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.factory = factories.CategoryFactory
        self.dummy_instance = self.factory.create()
        self.model = models.Category(
            id=self.dummy_instance.id,
            name=self.dummy_instance.name,
        )
        self.model_attributes = [
            'id',
            'name',
        ]


@pytest.mark.usefixtures('base_setup')
class TestTag(BaseModelTest):

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.factory = factories.TagFactory
        self.dummy_instance = self.factory.create()
        self.model = models.Tag(
            id=self.dummy_instance.id,
            name=self.dummy_instance.name,
        )
        self.model_attributes = [
            'id',
            'name',
        ]


@pytest.mark.usefixtures('base_setup')
class TestContent(BaseModelTest):

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.factory = factories.ContentFactory
        self.dummy_instance = self.factory.create()
        self.model = models.Content(
            id=self.dummy_instance.id,
            title=self.dummy_instance.title,
            created_date=self.dummy_instance.created_date,
            published_date=self.dummy_instance.published_date,
            updated_date=self.dummy_instance.updated_date,
            url=self.dummy_instance.url,
            score=self.dummy_instance.score,
            predicted_score=self.dummy_instance.predicted_score,
            predicted_certainty=self.dummy_instance.predicted_certainty,
        )

        self.model_attributes = [
            'id',
            'title',
            'created_date',
            'published_date',
            'updated_date',
            'url',
            'score',
            'predicted_score',
            'predicted_certainty',
        ]


@pytest.mark.usefixtures('base_setup')
class TestArticle(TestContent):

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.factory = factories.ArticleFactory
        self.dummy_instance = self.factory.create()
        self.model = models.Article(
            id=self.dummy_instance.id,
            title=self.dummy_instance.title,
            created_date=self.dummy_instance.created_date,
            published_date=self.dummy_instance.published_date,
            updated_date=self.dummy_instance.updated_date,
            url=self.dummy_instance.url,
            score=self.dummy_instance.score,
            predicted_score=self.dummy_instance.predicted_score,
            predicted_certainty=self.dummy_instance.predicted_certainty,
            source_id=self.dummy_instance.source_id,
            summary=self.dummy_instance.summary,
            body=self.dummy_instance.body,
            image_path=self.dummy_instance.image_path,
        )

        self.model_attributes = [
            'id',
            'title',
            'created_date',
            'published_date',
            'updated_date',
            'url',
            'score',
            'predicted_score',
            'predicted_certainty',
            'summary',
            'body',
            'image_path',
            'source_id',
        ]


@pytest.mark.usefixtures('base_setup')
class TestSource(BaseModelTest):

    @pytest.fixture(autouse=True)
    def setup(self, session):
        self.factory = factories.SourceFactory
        self.dummy_instance = self.factory.create()
        self.model = models.Source(
            id=self.dummy_instance.id,
            title=self.dummy_instance.title,
            description=self.dummy_instance.description,
            created_date=self.dummy_instance.created_date,
            published_date=self.dummy_instance.published_date,
            updated_date=self.dummy_instance.updated_date,
            url=self.dummy_instance.url,
            aggregated_score=self.dummy_instance.aggregated_score,
            aggregated_certainty=self.dummy_instance.aggregated_certainty,
        )

        self.model_attributes = [
            'id',
            'title',
            'description',
            'created_date',
            'published_date',
            'updated_date',
            'url',
            'aggregated_score',
            'aggregated_certainty',
        ]
