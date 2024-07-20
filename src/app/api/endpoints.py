from fastapi import APIRouter, status

import app.domain.storage.attachments.views
import app.domain.users.auth.views
import app.domain.meteo.views
import app.domain.users.profile.views
import app.domain.users.registration.views
from app.api import schemas

users_router = APIRouter(prefix="/authentication")
users_router.include_router(
    app.domain.users.registration.views.router,
    prefix="/v1",
    tags=["Authentication"],
)
users_router.include_router(
    app.domain.users.auth.views.router,
    prefix="/v1",
    tags=["Authentication"],
)

profile = APIRouter(prefix="/profile")
profile.include_router(
    app.domain.users.profile.views.router,
    prefix="/v1",
    tags=["Profile"],
)

meteo = APIRouter(prefix="/meteo")
meteo.include_router(
    app.domain.meteo.views.router,
    prefix="/v1",
    tags=["Meteo"],
)

router = APIRouter(
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": schemas.AuthApiError},
        status.HTTP_403_FORBIDDEN: {"model": schemas.SimpleApiError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": schemas.SimpleApiError},
    }
)

router.include_router(users_router)
router.include_router(profile)
router.include_router(meteo)
