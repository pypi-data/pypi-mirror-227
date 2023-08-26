import copy
from typing import List, Optional

from attr import define

from trendup_video.reader.video_reader import VideoReader
from trendup_video.recorded_video import RecordedVideo
from trendup_video.download.download_video import DownloadVideo
from trendup_video.web.pre_handle_video import PreHandleVideo
from trendup_video.web_recorded_video import WebRecordedVideo


@define
class PreHandleVideoImpl(PreHandleVideo):
    download_video: DownloadVideo
    video_reader: VideoReader

    def pre_handle_video(self, videos: List[WebRecordedVideo]) -> List[RecordedVideo]:
        result = []

        for video in videos:
            recorded_video = self._read_and_map_video(video)

            if recorded_video is not None and len(recorded_video.frames) > 0:
                result.append(recorded_video)

        return result

    def _read_and_map_video(self, video: WebRecordedVideo) -> Optional[RecordedVideo]:
        video_path = self.download_video.download(video.storage_reference)

        if video_path is None:
            return None

        try:
            video_info = self.video_reader.read_video(video_path)
        except Exception as e:
            return None

        return self.cut_video_to_match_timestamps(RecordedVideo(
            info=video_info,
            recorder_name=video.recorder_name,
            timestamps=video.timestamps
        ))

    def cut_video_to_match_timestamps(self, video: RecordedVideo) -> RecordedVideo:
        video_return = copy.deepcopy(video)
        timestamps = video.timestamps

        if len(video_return.frames) > len(timestamps):
            video_return.info.frames = video_return.frames[0:len(timestamps)]
        elif len(video_return.frames) < len(timestamps):
            video_return.timestamps = timestamps[0:len(video_return.frames)]

        return video_return
