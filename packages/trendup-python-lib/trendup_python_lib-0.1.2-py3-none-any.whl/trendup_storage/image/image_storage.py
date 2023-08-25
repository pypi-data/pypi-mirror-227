from abc import abstractmethod

from trendup_storage.models import StorageReference
from trendup_video.type_alias import Frame


class ImageStorage:

    @abstractmethod
    def save_image(self, image: Frame) -> StorageReference:
        pass

    @abstractmethod
    def load_image(self, reference: StorageReference) -> Frame:
        pass
