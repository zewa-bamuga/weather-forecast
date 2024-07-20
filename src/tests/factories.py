import factory

from app.domain.common import enums, models
from tests import utils


class AttachmentFactory(utils.AsyncSQLAlchemyModelFactory):
    name = factory.Faker("name")
    path = factory.Faker("name")
    uri = factory.Faker("uri")

    class Meta:
        model = models.Attachment


class UserFactory(utils.AsyncSQLAlchemyModelFactory):
    username = factory.Faker("name")
    email = factory.Faker("email")
    password_hash = factory.Faker("password")
    status = factory.Faker("random_element", elements=enums.UserStatuses)
    avatar_attachment = factory.SubFactory(AttachmentFactory)
    permissions = {}

    class Meta:
        model = models.User


class WeatherFactory(utils.AsyncSQLAlchemyModelFactory):
    city = factory.Faker("city")
    user_id = factory.SubFactory(UserFactory)

    class Meta:
        model = models.SearchHistory
