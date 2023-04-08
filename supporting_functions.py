import datetime
from tkinter import filedialog
import cv2

def chunks(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]


def pixels(height, width):
    for h in range(*height):
        for w in range(*width):
            yield h, w


def resize(sequence, scale_percent=100):
    width = int(sequence.shape[1] * scale_percent / 100)
    height = int(sequence.shape[0] * scale_percent / 100)

    current_size = (sequence.shape[1], sequence.shape[0])
    new_size = (width, height)

    interpolation = cv2.INTER_AREA if current_size < new_size else cv2.INTER_CUBIC
    output = cv2.resize(sequence, new_size, interpolation=interpolation)
    return output


def get_path(type_="File, Directory"):
    operations = {
        "File": (filedialog.askopenfile, "Choose file: "),
        "Directory": (filedialog.askdirectory, "Choose directory: ")
    }
    try:
        func = operations[type_][0]
        title = operations[type_][1]
        path = func(title=title)
        path = path.replace("/", "\\") if type_ == "Directory" else path.name.replace("/", "\\")
    except Exception as e:
        changelog(e)

    return path


def get_bytes(file):
    filename = file.rpartition("\\")[2]
    try:
        with open(file, "rb") as f:
            byte_array = list(f.read())
            changelog(f"Byte code for '{filename}' receive")
    except IOError as e:
        changelog(e)

    return byte_array


def changelog(log):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {log}")
