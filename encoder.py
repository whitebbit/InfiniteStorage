import asyncio
import time
import cv2
import numpy as np
from aiomultiprocess import Pool
from settings import VideoSettings
from supporting_functions import resize, pixels, chunks, get_path, get_bytes, changelog


class Encoder:
    settings = VideoSettings(1280, 720, 2)

    def __init__(self, path_to_file, output_path):
        self.path = path_to_file
        self.filename = path_to_file.rpartition("\\")[2]
        self.output = output_path

    def encode(self):
        t0 = time.time()
        changelog(f"Start of encoding '{self.filename}'")
        frames = asyncio.run(self.create_frames())
        self.create_video(frames)
        changelog(f"End of encoding '{self.filename}' in {'{:.2f}'.format(time.time() - t0)} seconds")

    async def create_frames(self):
        data = self.frames_data()

        async with Pool() as pool:
            results = await pool.map(self.create_frame, data)

        changelog(f"Frames for '{self.filename}' created")
        return results

    async def create_frame(self, data):
        binary = list("".join('{0:08b}'.format(s) for s in data))
        resolution = self.settings.resolution
        sequence = np.ndarray((resolution.height, resolution.width, 3), dtype=np.uint8)
        pixel = list(pixels([resolution.height], [resolution.width]))
        for b, p in zip(binary, pixel):
            color = int(b) * 255
            sequence[*p] = color
        else:
            if len(pixel) > len(binary):
                for p in pixel[len(binary):]:
                    sequence[*p] = 0

        frame = resize(sequence, self.settings.size * 100)
        return frame

    def create_video(self, frames):
        res = self.settings.actual_resolution
        resolution = [res.width, res.height]

        fourcc = cv2.VideoWriter_fourcc('a', 'v', 'c', '1')
        output_file = self.output + "\\" + self.filename + ".avi"
        video = cv2.VideoWriter(output_file, fourcc, 10, resolution)

        for frame in frames:
            try:
                video.write(frame)
            except Exception as e:
                changelog(e)

        video.release()
        changelog(f"Video '{self.filename}.avi' created")

    def frames_data(self):
        byte = get_bytes(self.path)
        resolution = self.settings.resolution
        max_len = int((resolution.width * resolution.height) / 8)

        frames_data = list(chunks(byte, max_len))
        return frames_data


def main():
    file = get_path("File")
    output = get_path("Directory")
    en = Encoder(file, output)
    en.encode()
