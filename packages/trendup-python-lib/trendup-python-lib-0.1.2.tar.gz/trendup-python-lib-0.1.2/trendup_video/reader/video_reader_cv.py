import cv2

from trendup_video.reader.video_reader import VideoReader
from trendup_video.video_data import VideoInfo


class VideoReaderCV(VideoReader):

    def read_video(self, path: str) -> VideoInfo:
        capture = cv2.VideoCapture(path)
        frames = []

        while True:
            ret, frame = capture.read()
            if not ret:
                break
            frames.append(frame)

        return VideoInfo(
            frames=frames,
            width=int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            height=int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            fps=int(capture.get(cv2.CAP_PROP_FPS)),
        )
