import tempfile
from unittest import TestCase

from tests.doubles.file_storage_mock import FileStorageMock
from tests.doubles.temp_file_stub import TempFileStub
from trendup_storage.file import StorageFileBasic
from trendup_storage.models import StorageReference
from trendup_video.download.download_video_impl import DownloadVideoImpl


class TestDownloadVideoImpl(TestCase):

    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.temp_file = TempFileStub(self.dir.name)
        self.file_storage = FileStorageMock()
        self.download_video = DownloadVideoImpl(
            temp_file=self.temp_file,
            file_storage=self.file_storage
        )

    def tearDown(self) -> None:
        self.dir.cleanup()

    def test_should_return_null_if_file_not_found(self):
        self.assertIsNone(
            self.download_video.download(storage_reference=StorageReference(env="LOCAL", id="not_found"))
        )

    def test_should_save_video_to_temp_file(self):
        reference = self.file_storage.save(StorageFileBasic(
            name="test",
            extension="mp4",
            content=b"test"
        ))

        self.assertEqual(
            self.temp_file.path + ".mp4",
            self.download_video.download(reference)
        )
