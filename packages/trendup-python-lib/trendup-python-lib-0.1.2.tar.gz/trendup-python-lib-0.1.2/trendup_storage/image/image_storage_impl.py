import cv2
import numpy as np
from attr import define

from trendup_storage.file import StorageFileBasic
from trendup_storage.file_storage import FileStorage
from trendup_storage.image.image_storage import ImageStorage
from trendup_storage.models import StorageReference
from trendup_video.type_alias import Frame


@define
class ImageStorageImpl(ImageStorage):
    storage: FileStorage

    def save_image(self, image: Frame) -> StorageReference:
        img_bytes = cv2.imencode('.jpg', image)[1].tobytes()

        return self.storage.save(StorageFileBasic(
            name='image',
            extension='jpg',
            content=img_bytes
        ))

    def load_image(self, reference: StorageReference) -> Frame:
        file_bytes = self.storage.load(reference).read()
        np_arr = np.frombuffer(file_bytes, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
