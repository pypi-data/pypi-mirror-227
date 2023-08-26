from abc import abstractmethod
from typing import Optional

from trendup_storage.models import StorageReference


class DownloadVideo:

    @abstractmethod
    def download(self, storage_reference: StorageReference) -> Optional[str]:
        pass
