from typing import List

from attr import define

from trendup_storage.models import StorageReference


@define
class WebRecordedVideo:
    recorder_name: str
    storage_reference: StorageReference
    timestamps: List[int]
