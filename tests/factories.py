from airss_dl import models

import factory

# XXX If you add new Factories remember to add the session in conftest.py


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake author element.
    """
    id = factory.Faker('random_number')
    name = factory.Faker('name')

    class Meta:
        model = models.Author
        sqlalchemy_session_persistence = 'commit'


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake category element.
    """
    id = factory.Faker('random_number')
    name = factory.Faker('name')

    class Meta:
        model = models.Category
        sqlalchemy_session_persistence = 'commit'


class TagFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake tag element.
    """
    id = factory.Faker('random_number')
    name = factory.Faker('name')

    class Meta:
        model = models.Tag
        sqlalchemy_session_persistence = 'commit'


class SourceFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake source element.
    """
    id = factory.Sequence(lambda n: n)
    title = factory.Faker('sentence')
    description = factory.Faker('sentence')
    created_date = factory.Faker('date_time')
    updated_date = factory.Faker('date_time')
    url = factory.Faker('url')
    aggregated_score = factory.Faker('pyfloat')
    aggregated_certainty = factory.Faker('pyfloat')

    class Meta:
        model = models.Source
        sqlalchemy_session_persistence = 'commit'


class RssSourceFactory(SourceFactory):
    """
    Class to generate a fake rss source element.
    """
    image_path = factory.Faker('file_path')

    class Meta:
        model = models.RssSource
        sqlalchemy_session_persistence = 'commit'


class ContentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake content element.
    """
    id = factory.Sequence(lambda n: n)
    title = factory.Faker('sentence')
    published_date = factory.Faker('date_time')
    created_date = factory.Faker('date_time')
    updated_date = factory.Faker('date_time')
    url = factory.Faker('url')
    score = factory.Faker('random_number')
    predicted_score = factory.Faker('pyfloat')
    predicted_certainty = factory.Faker('pyfloat')

    class Meta:
        model = models.Content
        sqlalchemy_session_persistence = 'commit'


class ArticleFactory(ContentFactory):
    """
    Class to generate a fake article element.
    """
    source_id = factory.Faker('word')
    summary = factory.Faker('sentence')
    body = factory.Faker('sentence')
    image_path = factory.Faker('file_path')

    class Meta:
        model = models.Article
        sqlalchemy_session_persistence = 'commit'
