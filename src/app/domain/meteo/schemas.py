import enum
from dataclasses import dataclass
from typing import List
from uuid import UUID

from a8t_tools.db import pagination as pg
from a8t_tools.db import sorting as sr

from app.domain.common.schemas import APIModel


class SearchHistoryCreate(APIModel):
    user_id: UUID
    city: str


class CityCount(APIModel):
    city: str
    count: int


class CurrentWeather(APIModel):
    time: str
    temperature_2m: float
    wind_speed_10m: float


class HourlyWeather(APIModel):
    time: List[str]
    temperature_2m: List[float]
    relative_humidity_2m: List[int]
    wind_speed_10m: List[float]


class WeatherResponse(APIModel):
    current: CurrentWeather
    hourly: HourlyWeather


class SearchHistorySorts(enum.StrEnum):
    id = enum.auto()
    city = enum.auto()
    user_id = enum.auto()
    created_at = enum.auto()


@dataclass
class SearchHistoryListRequestSchema:
    pagination: pg.PaginationCallable[SearchHistoryCreate] | None = None
    sorting: sr.SortingData[SearchHistorySorts] | None = None


@dataclass
class SearchHistoryWhere:
    id: UUID | None = None
    user_id: UUID | None = None
