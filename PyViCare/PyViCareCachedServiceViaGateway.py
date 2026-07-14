import logging
from typing import Any

from PyViCare.PyViCareAbstractOAuthManager import AbstractViCareOAuthManager
from PyViCare.PyViCareCachedServiceBase import ViCareCachedServiceBase
from PyViCare.PyViCareService import ViCareDeviceAccessor
from PyViCare.PyViCareServiceViaGateway import (
    ViCareServiceViaGateway, filter_features_for_device)

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ViCareCachedServiceViaGateway(ViCareCachedServiceBase, ViCareServiceViaGateway):
    """Cached variant of the gateway bulk-fetch service.

    One instance is shared across all devices on the gateway; every device's
    getProperty reads from the same cached bulk payload. setProperty clears the
    whole cache.
    """

    def __init__(self, oauth_manager: AbstractViCareOAuthManager, cacheDuration: int) -> None:  # pylint: disable=super-init-not-called
        ViCareServiceViaGateway.__init__(self, oauth_manager)
        self._init_cache(cacheDuration)

    def _fetch_uncached(self, accessor: ViCareDeviceAccessor) -> Any:
        return ViCareServiceViaGateway.fetch_all_features(self, accessor)

    def _extract_entities(self, data: dict, accessor: ViCareDeviceAccessor) -> list[dict[str, Any]]:
        return filter_features_for_device(data["data"], accessor.device_id)

    def fetch_all_features(self, accessor: ViCareDeviceAccessor) -> Any:
        # cached too, so per-device coordinators share one bulk fetch
        return self._get_or_update_cache(accessor)
