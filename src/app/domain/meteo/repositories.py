from typing import List, TypeVar
from uuid import UUID

from a8t_tools.db.pagination import PaginationCallable, Paginated, NoPaginationResults
from a8t_tools.db.sorting import SortingData, SortFieldType, apply_sorting
from a8t_tools.db.transactions import AsyncDbTransaction
from a8t_tools.db.utils import CrudRepositoryMixin
from pydantic import BaseModel
from sqlalchemy import ColumnElement, and_, select, func
from sqlalchemy.sql.base import ExecutableOption

from app.domain.common import models
from app.domain.common.schemas import IdContainer
from app.domain.meteo import schemas

Schema = TypeVar("Schema", bound=BaseModel)


class MeteoRepository(CrudRepositoryMixin[models.SearchHistory]):
    def __init__(self, transaction: AsyncDbTransaction):
        self.model = models.SearchHistory
        self.transaction = transaction

    async def create_meteo_history(self, payload: schemas.SearchHistoryCreate) -> IdContainer:
        return IdContainer(id=await self._create(payload))

    async def get_meteo_history(
            self,
            pagination: PaginationCallable[schemas.SearchHistoryCreate] | None = None,
            sorting: SortingData[schemas.SearchHistorySorts] | None = None,
            user_id: UUID | None = None,
    ) -> Paginated[schemas.SearchHistoryCreate]:
        return await self._get_modified_list(
            schemas.SearchHistoryCreate,
            pagination=pagination,
            sorting=sorting,
            condition=self._create_user_filter(user_id)
        )

    async def get_city_counts(self) -> dict[str, int]:
        stmt = (
            select(
                self.model.city,
                func.count().label('count')
            )
            .group_by(self.model.city)
        )
        async with self.transaction.use() as db:
            result = await db.execute(stmt)
            city_counts = result.all()
            return {city: count for city, count in city_counts}

    async def get_meteo_history_by_filter(
            self,
            where: schemas.SearchHistoryWhere
    ) -> List[schemas.SearchHistoryCreate]:
        return await self._get_many(
            schema=schemas.SearchHistoryCreate,
            condition=await self._format_filters(where),
        )

    async def _format_filters(self, where: schemas.SearchHistoryWhere) -> ColumnElement[bool]:
        filters: list[ColumnElement[bool]] = []

        if where.id is not None:
            filters.append(models.SearchHistory.id == where.id)

        if where.user_id is not None:
            filters.append(models.SearchHistory.user_id == where.user_id)

        return and_(*filters)

    async def _get_modified_list(
            self,
            schema: type[Schema],
            pagination: PaginationCallable[Schema] | None = None,
            sorting: SortingData[SortFieldType] | None = None,
            condition: ColumnElement[bool] | None = None,
            options: list[ExecutableOption] | None = None,
    ) -> Paginated[Schema]:
        stmt = (
            select(self.model)
            .distinct(self.model.city)
            .order_by(self.model.city, self.model.id)
        )

        if condition is not None:
            stmt = stmt.where(condition)
        if sorting is not None:
            stmt = apply_sorting(stmt, sorting)
        if options is not None:
            stmt = stmt.options(*options)

        async with self.transaction.use() as db:
            if pagination is None:
                results = (await db.execute(stmt)).scalars().all()
                return NoPaginationResults([schema.model_validate(x) for x in results])

            return await pagination(db, stmt)

    def _create_user_filter(self, user_id: UUID | None) -> ColumnElement[bool] | None:
        if user_id is None:
            return None
        return self.model.user_id == user_id

    async def _get_many(
            self,
            schema: type[Schema],
            *,
            condition: ColumnElement[bool] | None = None,
            options: List[ExecutableOption] | None = None,
    ) -> List[Schema]:
        stmt = select(self.model)
        if condition is not None:
            stmt = stmt.where(condition)
        if options is not None:
            stmt = stmt.options(*options)

        async with self.transaction.use() as db:
            result = await db.execute(stmt)
            results = result.scalars().all()
            return [schema.model_validate(item) for item in results]
