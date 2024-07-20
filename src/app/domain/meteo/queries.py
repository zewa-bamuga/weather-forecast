import datetime
from uuid import UUID

from a8t_tools.db.pagination import Paginated
from fastapi import HTTPException
from httpx import AsyncClient

from app.domain.meteo import schemas
from app.domain.meteo.commands import SearchHistoryCreateCommand
from app.domain.meteo.repositories import MeteoRepository
from app.domain.meteo.schemas import SearchHistoryCreate, SearchHistoryListRequestSchema
from app.domain.users.permissions.services import UserPermissionService
from app.domain.users.profile.queries import UserProfileMeQuery

GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"


class CurrentCoordinatesQuery:
    def __init__(
            self,
            current_user_query: UserProfileMeQuery,
            search_history_create_command: SearchHistoryCreateCommand,

    ):
        self.client = AsyncClient()
        self.current_user_query = current_user_query
        self.search_history_create_command = search_history_create_command

    async def __call__(self, city: str) -> dict:
        current_user = await self.current_user_query()

        geocoding_response = await self.client.get(
            GEOCODING_API_URL,
            params={"q": city, "format": "json"}
        )

        if geocoding_response.status_code != 200:
            raise HTTPException(status_code=geocoding_response.status_code, detail="Failed to fetch geocoding data")

        geocoding_data = geocoding_response.json()
        if not geocoding_data or not isinstance(geocoding_data, list):
            raise HTTPException(status_code=404, detail="City not found")

        latitude = geocoding_data[0]["lat"]
        longitude = geocoding_data[0]["lon"]

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m"
        }

        weather_response = await self.client.get(WEATHER_API_URL, params=weather_params)

        if weather_response.status_code != 200:
            raise HTTPException(status_code=weather_response.status_code, detail="Failed to fetch weather data")

        weather_data = weather_response.json()

        current_date = datetime.datetime.utcnow().date()
        hourly_data = weather_data.get("hourly", {})
        times = hourly_data.get("time", [])
        temperatures = hourly_data.get("temperature_2m", [])
        humidities = hourly_data.get("relative_humidity_2m", [])
        wind_speeds = hourly_data.get("wind_speed_10m", [])

        filtered_data = {
            "time": [],
            "temperature_2m": [],
            "relative_humidity_2m": [],
            "wind_speed_10m": []
        }

        for i, time_str in enumerate(times):
            time_obj = datetime.datetime.fromisoformat(time_str)
            if time_obj.date() == current_date:
                filtered_data["time"].append(time_str)
                filtered_data["temperature_2m"].append(temperatures[i])
                filtered_data["relative_humidity_2m"].append(humidities[i])
                filtered_data["wind_speed_10m"].append(wind_speeds[i])

        await self.search_history_create_command(
            SearchHistoryCreate(
                user_id=current_user.id,
                city=city,
            )
        )

        return filtered_data


class CityListQuery:
    def __init__(self, meteo_repository: MeteoRepository):
        self.meteo_repository = meteo_repository

    async def __call__(self, payload: schemas.SearchHistoryListRequestSchema) -> dict[str, int]:
        return await self.meteo_repository.get_city_counts()


class SearchHistoryListQuery:
    def __init__(self, meteo_repository: MeteoRepository):
        self.meteo_repository = meteo_repository

    async def __call__(self, payload: schemas.SearchHistoryListRequestSchema, user_id: UUID) -> Paginated[
        schemas.SearchHistoryCreate]:
        return await self.meteo_repository.get_meteo_history(payload.pagination, payload.sorting, user_id)


class CityManagementListQuery:
    def __init__(
            self,
            permission_service: UserPermissionService,
            query: CityListQuery,
    ) -> None:
        self.query = query
        self.permission_service = permission_service

    async def __call__(self, payload: SearchHistoryListRequestSchema) -> dict[str, int]:
        return await self.query(payload)


class HistoryCityManagementListQuery:
    def __init__(
            self,
            query: SearchHistoryListQuery,
            current_user_query: UserProfileMeQuery,
            meteo_repository: MeteoRepository
    ) -> None:
        self.query = query
        self.current_user_query = current_user_query
        self.meteo_repository = meteo_repository

    async def __call__(self, payload: SearchHistoryListRequestSchema) -> Paginated[SearchHistoryCreate]:
        current_user = await self.current_user_query()
        search_history = await self.meteo_repository.get_meteo_history_by_filter(
            schemas.SearchHistoryWhere(user_id=current_user.id))
        assert search_history
        return await self.query(payload, current_user.id)
