import factory

from models_app.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker('name'),
    description = factory.Faker('sentence'),
