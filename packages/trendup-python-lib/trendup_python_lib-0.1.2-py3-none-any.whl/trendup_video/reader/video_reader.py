from abc import abstractmethod

from trendup_video.video_data import VideoInfo


class VideoReader:

    @abstractmethod
    def read_video(self, path: str) -> VideoInfo:
        pass
