from collections import namedtuple

resolution = namedtuple("Resolution", ["width", "height"])


class VideoSettings:
    def __init__(self, width, height, size):
        self.size = size
        self.resolution = resolution(width=int(width / size), height=int(height / size))
        self.actual_resolution = resolution(width=width, height=height)

