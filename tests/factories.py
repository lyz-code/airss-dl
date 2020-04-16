from airss_downloader import models

import factory

# XXX If you add new Factories remember to add the session in conftest.py


class AuthorFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake author element.
    """
    id = factory.Faker('word')
    name = factory.Faker('name')

    class Meta:
        model = models.Author
        sqlalchemy_session_persistence = 'commit'


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake category element.
    """
    id = factory.Faker('word')
    name = factory.Faker('name')

    class Meta:
        model = models.Category
        sqlalchemy_session_persistence = 'commit'


class TagFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake tag element.
    """
    id = factory.Faker('word')
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
    published_date = factory.Faker('date_time')
    updated_date = factory.Faker('date_time')
    url = factory.Faker('url')
    aggregated_score = factory.Faker('pyfloat')
    aggregated_certainty = factory.Faker('pyfloat')

    class Meta:
        model = models.Source
        sqlalchemy_session_persistence = 'commit'


class ContentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake content element.
    """
    id = factory.Sequence(lambda n: n)
    title = factory.Faker('sentence')
    created_date = factory.Faker('date_time')
    published_date = factory.Faker('date_time')
    updated_date = factory.Faker('date_time')
    url = factory.Faker('url')
    author = factory.SubFactory(AuthorFactory)
    score = factory.Faker('random_number')
    predicted_score = factory.Faker('pyfloat')
    predicted_certainty = factory.Faker('pyfloat')

    class Meta:
        model = models.Content
        sqlalchemy_session_persistence = 'commit'
