from typing import Tuple, List

from attr import attr, Factory, define

from trendup_storage.image.image_storage import ImageStorage
from trendup_storage.models import StorageReference
from trendup_video.type_alias import Frame


@define
class ImageStorageMock(ImageStorage):
    res_map: List[Tuple[Frame, StorageReference]] = attr(default=Factory(list))

    def save_image(self, image: Frame) -> StorageReference:
        for frame, reference in self.res_map:
            if frame.all() == image.all():
                return reference

        raise ValueError(f"Image {image} not found")

    def load_image(self, reference: StorageReference) -> Frame:
        for frame, ref in self.res_map:
            if ref == reference:
                return frame

        raise ValueError(f"Reference {reference} not found")

    def set_response(self, frame: Frame, reference: StorageReference):
        self.res_map.append((frame, reference))
