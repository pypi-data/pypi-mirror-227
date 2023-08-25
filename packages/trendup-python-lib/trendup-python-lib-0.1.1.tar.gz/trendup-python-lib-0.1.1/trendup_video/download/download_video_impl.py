from typing import Optional

from attr import define

from trendup_storage.file_storage import FileStorage
from trendup_storage.models import StorageReference
from trendup_utils.temp_file import TempFile
from trendup_video.download.download_video import DownloadVideo


@define
class DownloadVideoImpl(DownloadVideo):
    temp_file: TempFile
    file_storage: FileStorage

    def download(self, storage_reference: StorageReference) -> Optional[str]:
        file = self.file_storage.load(storage_reference)

        if file is None:
            return None

        temp_path = self.temp_file.make_temp_file_path() + f".{file.get_extension()}"

        with open(temp_path, "wb") as temp_file:
            temp_file.write(file.read())

        return temp_path
