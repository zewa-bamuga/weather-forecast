from contextlib import asynccontextmanager

from a8t_tools.security.tokens import override_user_token
from a8t_tools.db import pagination, sorting
from dependency_injector import wiring
from fastapi import APIRouter, Query, Header, Depends

from app.api import deps
from app.containers import Container
from app.domain.meteo import schemas
from app.domain.meteo.queries import CurrentCoordinatesQuery, HistoryCityManagementListQuery, CityManagementListQuery
from app.domain.meteo.schemas import HourlyWeather

router = APIRouter()


@asynccontextmanager
async def user_token(token: str):
    async with override_user_token(token or ""):
        yield


@router.post(
    "/weather",
    response_model=HourlyWeather,
)
@wiring.inject
async def get_weather(
        token: str = Header(...),
        city: str = Query(...),
        command: CurrentCoordinatesQuery = Depends(wiring.Provide[Container.user.coordinates_by_city_query]),
) -> HourlyWeather:
    async with user_token(token):
        weather_data = await command(city)
        return HourlyWeather(**weather_data)


@router.get(
    "/5_cityes",
    response_model=pagination.CountPaginationResults[schemas.SearchHistoryCreate],
)
@wiring.inject
async def get_last_5_cities(
        token: str = Header(...),
        query: HistoryCityManagementListQuery = Depends(
            wiring.Provide[Container.user.history_city_management_list_query]),
        pagination: pagination.PaginationCallable[schemas.SearchHistoryCreate] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.SearchHistoryCreate)),
        sorting: sorting.SortingData[schemas.SearchHistorySorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.SearchHistorySorts,
                schemas.SearchHistorySorts.user_id,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.SearchHistoryCreate]:
    async with user_token(token):
        return await query(schemas.SearchHistoryListRequestSchema(pagination=pagination, sorting=sorting))


@router.get(
    "/list",
    response_model=dict[str, int],
)
@wiring.inject
async def get_city_list(
        token: str = Header(...),
        query: CityManagementListQuery = Depends(
            wiring.Provide[Container.user.city_management_list_query]
        ),
) -> dict[str, int]:
    async with user_token(token):
        return await query(payload=schemas.SearchHistoryListRequestSchema())
