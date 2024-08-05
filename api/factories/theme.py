import factory
from factory.fuzzy import FuzzyInteger
from models_app.models import Theme


class ThemeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Theme

    name = factory.Faker('name')
    description = factory.Faker('sentence')
    image = factory.Faker('image_url')
    rating = FuzzyInteger(0, 50)