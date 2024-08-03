import factory
from factory.django import DjangoModelFactory
from .models import Collection, Movie
from django.contrib.auth.models import User
import uuid

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class MovieFactory(DjangoModelFactory):
    class Meta:
        model = Movie

    uuid = factory.LazyAttribute(lambda _: str(uuid.uuid4()))
    title = factory.Faker('sentence')
    description = factory.Faker('text')
    genres = factory.Faker('word')

class CollectionFactory(DjangoModelFactory):
    class Meta:
        model = Collection

    title = factory.Faker('sentence')
    description = factory.Faker('text')
    user = factory.SubFactory(UserFactory)
