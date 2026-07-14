import logging
from typing import Any, List

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareCachedServiceBase import ViCareCachedServiceBase
from PyViCare.PyViCareService import ViCareDeviceAccessor, ViCareService

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ViCareCachedService(ViCareCachedServiceBase, ViCareService):

    def __init__(self, oauth_manager: AbstractViCareOAuthManager, roles: List[str], cacheDuration: int) -> None:
        ViCareService.__init__(self, oauth_manager, roles)
        self._init_cache(cacheDuration)

    def _fetch_uncached(self, accessor: ViCareDeviceAccessor) -> Any:
        return ViCareService.fetch_all_features(self, accessor)

    def _extract_entities(self, data: dict, accessor: ViCareDeviceAccessor) -> list[dict[str, Any]]:
        entities: list[dict[str, Any]] = data["data"]
        return entities
