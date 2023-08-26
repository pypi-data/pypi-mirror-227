import tempfile
from pathlib import Path
from unittest import TestCase

from tests.stubs import Stubs
from trendup_storage.image.image_storage_impl import ImageStorageImpl
from trendup_storage.local_storage import FileStorageLocal


class TestImageStorageImpl(TestCase):

    def test_should_save_and_load_image(self):
        with tempfile.TemporaryDirectory() as directory:
            storage = FileStorageLocal(Path(directory))
            storage = ImageStorageImpl(storage)
            frame = Stubs.frame()

            reference = storage.save_image(frame)

            self.assertEqual(frame.all(), storage.load_image(reference).all())
