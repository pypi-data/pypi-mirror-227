from abc import abstractmethod
from typing import List

from trendup_video.recorded_video import RecordedVideo
from trendup_video.web_recorded_video import WebRecordedVideo


class PreHandleVideo:

    @abstractmethod
    def pre_handle_video(self, videos: List[WebRecordedVideo]) -> List[RecordedVideo]:
        pass
