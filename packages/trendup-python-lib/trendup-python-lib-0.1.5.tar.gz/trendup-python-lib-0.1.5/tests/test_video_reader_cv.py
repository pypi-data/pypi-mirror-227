from os.path import join
from unittest import TestCase

from tests.assets import Assets
from trendup_video.reader.video_reader_cv import VideoReaderCV


class TestVideoReaderCV(TestCase):

    def test_should_read_video(self):
        reader = VideoReaderCV()
        folder = join(Assets.get_assets_folder())
        info = reader.read_video(join(folder, "video.mp4"))

        self.assertEqual(info.fps, 30)
        self.assertEqual(info.width, 640)
        self.assertEqual(info.height, 480)
        self.assertEqual(len(info.frames), 6)
