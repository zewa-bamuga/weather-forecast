from uuid import uuid4

import pytest

from app.containers import Container
from tests import factories, utils


@utils.async_methods_in_db_transaction
class TestProfile:
    @pytest.fixture(autouse=True)
    def setup(self, client: utils.TestClientSessionExpire) -> None:
        self.client = client

    async def test_get_me(self, token_headers_factory):
        user = factories.UserFactory.create()
        headers = await token_headers_factory(user)
        response = await self.client.get("/api/profile/v1/me", headers=headers)
        assert response.status_code == 200

    async def test_get_me_not_auth(self):
        response = await self.client.get("/api/profile/v1/me")
        assert response.status_code == 422

    async def test_get_me_expired_token(self, container: Container):
        user = factories.UserFactory.create()
        token = await container.user.jwt_rsa_service(access_expiration_time=0).encode({"sub": str(user.id)}, "access")
        response = await self.client.get("/api/profile/v1/me", headers={"token": token})
        assert response.status_code == 401

    async def test_get_me_not_found(self, container: Container):
        token = await container.user.jwt_rsa_service().encode({"sub": str(uuid4())}, "access")
        response = await self.client.get("/api/profile/v1/me", headers={"token": token})
        assert response.status_code == 401
