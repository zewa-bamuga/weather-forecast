from app.domain.meteo import schemas
from app.domain.meteo.repositories import MeteoRepository


class SearchHistoryCreateCommand:
    def __init__(
            self,
            meteo_repository: MeteoRepository,
    ):
        self.meteo_repository = meteo_repository

    async def __call__(self, payload: schemas.SearchHistoryCreate) -> schemas.SearchHistoryCreate:
        search_history_id_container = await self.meteo_repository.create_meteo_history(
            schemas.SearchHistoryCreate(
                **payload.model_dump(),
            )
        )
