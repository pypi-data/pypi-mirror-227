from unittest import TestCase

from tests.stubs import Stubs
from trendup_video.recorded_video import RecordedVideo, IndexedFrame


class TestRecordedVideo(TestCase):

    def test_closest_frame_of_timestamp(self):
        with self.subTest("no timestamps"):
            video = self._create_video_with_timestamps([])

            with self.assertRaises(IndexError):
                video.closest_frame_of_timestamp(0)

        with self.subTest("one timestamp"):
            video = self._create_video_with_timestamps([0])
            self.assertFrameResult(0, video, 0)
            self.assertFrameResult(1, video, 0)
            self.assertFrameResult(-1, video, 0)

        with self.subTest("two or more timestamps"):
            video = self._create_video_with_timestamps([0, 10, 20, 30, 40])
            self.assertFrameResult(0, video, 0)
            self.assertFrameResult(10, video, 1)

            self.assertFrameResult(9, video, 1)
            self.assertFrameResult(19, video, 2)

            self.assertFrameResult(31, video, 3)
            self.assertFrameResult(1, video, 0)

            self.assertFrameResult(-1, video, 0)
            self.assertFrameResult(100, video, 4)

    def assertFrameResult(self, num: int, video: RecordedVideo, index: int):
        if index == -1:
            self.assertIsNone(video.closest_frame_of_timestamp(num))
            return

        self.assertEqual(IndexedFrame(Stubs.frame(index), index), video.closest_frame_of_timestamp(num))

    def _create_video_with_timestamps(self, timestamps: list[int]) -> RecordedVideo:
        info = Stubs.video_info()
        info.frames = [Stubs.frame(i) for i in range(len(timestamps))]

        return RecordedVideo(
            info=info,
            recorder_name="test",
            timestamps=timestamps
        )
