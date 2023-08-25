from typing import List, Tuple

from attr import define

from trendup_video.recorded_video import RecordedVideo
from trendup_video.web.pre_handle_video import PreHandleVideo
from trendup_video.web_recorded_video import WebRecordedVideo


@define
class PreHandleVideoMock(PreHandleVideo):
    res_map: List[Tuple[List[WebRecordedVideo], List[RecordedVideo]]] = []

    def pre_handle_video(self, videos: List[WebRecordedVideo]) -> List[RecordedVideo]:
        for entry in self.res_map:
            if entry[0] == videos:
                return entry[1]
        raise ValueError("No response for: " + str(videos))

    def set_response(self, videos: List[WebRecordedVideo], result: List[RecordedVideo]):
        self.res_map.append((videos, result))
