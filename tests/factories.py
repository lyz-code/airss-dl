from airss_downloader.models import \
    Contents, \
    Sources

import factory

# XXX If you add new Factories remember to add the session in conftest.py


class SourcesFactory(factory.alchemy.SQLAlchemyModelFactory):
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

    class Meta:
        model = Sources
        sqlalchemy_session_persistence = 'commit'


class ContentsFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Class to generate a fake content element.
    """
    id = factory.Sequence(lambda n: n)
    title = factory.Faker('sentence')
    created_date = factory.Faker('date_time')
    published_date = factory.Faker('date_time')
    updated_date = factory.Faker('date_time')
    url = factory.Faker('url')
    author_id = factory.Faker('random_number')

    class Meta:
        model = Contents
        sqlalchemy_session_persistence = 'commit'
