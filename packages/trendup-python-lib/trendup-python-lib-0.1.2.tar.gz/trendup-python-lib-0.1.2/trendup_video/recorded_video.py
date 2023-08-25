import numpy
from attr import define, field, cmp_using

from trendup_video.type_alias import Frame
from trendup_video.video_data import VideoInfo


@define
class RecordedVideo:
    info: VideoInfo
    recorder_name: str
    timestamps: list[int]

    @property
    def frames(self):
        return self.info.frames

    @property
    def width(self):
        return self.info.width

    @property
    def height(self):
        return self.info.height

    def closest_frame_of_timestamp(self, timestamp: int) -> 'IndexedFrame':
        index = self._closest_frame_index_of_timestamp(timestamp)

        if index == -1:
            raise IndexError("No frames in video")

        return IndexedFrame(
            frame=self.frames[index],
            index=index
        )

    def _closest_frame_index_of_timestamp(self, timestamp: int) -> int:
        if len(self.timestamps) == 0:
            return -1
        if len(self.timestamps) == 1:
            return 0

        # Implement binary search.
        left, right = 0, len(self.timestamps) - 1
        while left < right:
            mid = (left + right) // 2

            if self.timestamps[mid] == timestamp:
                return mid
            elif self.timestamps[mid] < timestamp:
                left = mid + 1
            else:
                right = mid

        # At this point, "left" is the closest frame.
        # Now, check if the previous frame is closer.
        if left > 0 and timestamp - self.timestamps[left - 1] < self.timestamps[left] - timestamp:
            return left - 1
        return left


@define
class IndexedFrame:
    frame: Frame = field(eq=cmp_using(eq=numpy.array_equal))
    index: int
