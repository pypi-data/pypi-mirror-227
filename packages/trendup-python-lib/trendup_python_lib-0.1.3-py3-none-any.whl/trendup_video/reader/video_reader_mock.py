from typing import List, Tuple

from attr import define, attr, Factory

from trendup_video.reader.video_reader import VideoReader
from trendup_video.video_data import VideoInfo


@define
class VideoReaderMock(VideoReader):
    response_maps: List[Tuple[str, VideoInfo]] = attr(default=Factory(list))
    error_maps: List[Tuple[str, Exception]] = attr(default=Factory(list))

    def read_video(self, path: str) -> VideoInfo:
        for video_path, error in self.error_maps:
            if video_path == path:
                raise error

        for video_path, video_info in self.response_maps:
            if video_path == path:
                return video_info

        raise Exception(f"Video {path} not found")

    def set_response(self, path: str, video_info: VideoInfo):
        self.response_maps.append((path, video_info))

    def set_error(self, path: str, error: Exception):
        self.error_maps.append((path, error))
