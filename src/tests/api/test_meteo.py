import pytest

from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestMeteo:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    async def test_post_city_list(self, token_headers_factory):
        user = factories.UserFactory.create()
        headers = await token_headers_factory(user)
        response = await self.client.post("/api/meteo/v1/weather?city=London", headers=headers)
        assert response.status_code == 200

    async def test_get_last_5_cities(self, token_headers_factory):
        user = factories.UserFactory.create()
        headers = await token_headers_factory(user)

        for _ in range(6):
            factories.WeatherFactory.create(user_id=user.id)

        response = await self.client.get("/api/meteo/v1/5_cityes", headers=headers)

        assert response.status_code == 200
        data = response.json()

        assert "items" in data
        assert len(data["items"]) == 5
        assert data["count"] == 6

        for item in data["items"]:
            assert "city" in item
            assert "userId" in item

    async def test_get_city_list(self, token_headers_factory):
        user = factories.UserFactory.create()
        headers = await token_headers_factory(user)

        city_names = ["CityA", "CityB", "CityC"]
        for city in city_names:
            factories.WeatherFactory.create(user_id=user.id, city=city)

        response = await self.client.get("/api/meteo/v1/list", headers=headers)

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, dict)
        for city in city_names:
            assert city in data
            assert isinstance(data[city], int)
