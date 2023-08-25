from typing import List

import attr
import numpy

from trendup_video.type_alias import Frame


@attr.define
class VideoInfo:
    frames: List[Frame] = attr.field(eq=attr.cmp_using(eq=numpy.array_equal))
    width: int
    height: int
    fps: int

    @property
    def interval(self) -> int:
        return int(1000 / self.fps)
