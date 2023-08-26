import copy
from unittest import TestCase

from tests.doubles.download_video_mock import DownloadVideoMock
from tests.doubles.video_reader import VideoReaderMock
from tests.stubs import Stubs
from tests.web_stubs import WebStubs
from trendup_video.recorded_video import RecordedVideo
from trendup_video.web.pre_handle_video_impl import PreHandleVideoImpl


class TestPreHandleVideoImpl(TestCase):

    def setUp(self) -> None:
        self.download_video = DownloadVideoMock()
        self.video_reader = VideoReaderMock()
        self.pre_handle_video = PreHandleVideoImpl(self.download_video, self.video_reader)

        self.web_video = WebStubs.recorded_video("LEFT")

    def test_should_ignore_if_can_not_download(self):
        self.download_video.set_response(self.web_video.storage_reference, None)
        self.assertEqual(self.pre_handle_video.pre_handle_video([self.web_video]), [])

    def test_should_ignore_if_can_not_read(self):
        self.download_video.set_response(self.web_video.storage_reference, "video.mp4")
        self.video_reader.set_error("video.mp4", Exception("Can not read video"))

        self.assertEqual(self.pre_handle_video.pre_handle_video([self.web_video]), [])

    def test_should_ignore_empty_videos(self):
        empty_frame_video = Stubs.video_info()
        empty_frame_video.frames = []
        self.download_video.set_response(self.web_video.storage_reference, "video.mp4")
        self.video_reader.set_response("video.mp4", empty_frame_video)

        self.assertEqual(self.pre_handle_video.pre_handle_video([self.web_video]), [])

    def test_should_cut_timestamps_if_longer(self):
        self.web_video.timestamps = [1, 2, 3, 4, 5]
        videos_with_less_frame = Stubs.video_info()
        videos_with_less_frame.frames = [Stubs.frame(0), Stubs.frame(1), Stubs.frame(2)]

        self.download_video.set_response(self.web_video.storage_reference, "video.mp4")
        self.video_reader.set_response("video.mp4", videos_with_less_frame)

        self.assertEqual(self.pre_handle_video.pre_handle_video([self.web_video]), [RecordedVideo(
            info=videos_with_less_frame,
            recorder_name="LEFT",
            timestamps=[1, 2, 3]
        )])

    def test_should_cut_frames_if_longer(self):
        self.web_video.timestamps = [1, 2, 3]
        more_frame = Stubs.video_info()
        more_frame.frames = [Stubs.frame(0), Stubs.frame(1), Stubs.frame(2), Stubs.frame(3), Stubs.frame(4)]

        expected_video = copy.deepcopy(more_frame)
        expected_video.frames = expected_video.frames[0:3]

        self.download_video.set_response(self.web_video.storage_reference, "video.mp4")
        self.video_reader.set_response("video.mp4", more_frame)

        self.assertEqual(self.pre_handle_video.pre_handle_video([self.web_video]), [RecordedVideo(
            info=expected_video,
            recorder_name="LEFT",
            timestamps=[1, 2, 3]
        )])
