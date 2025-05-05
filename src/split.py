import os


def get_frame_lines(filename):
    with open(filename) as f:
        first = f.readline()
    N = int(first.strip())
    return N + 2


def split_xyz(input_file: str, frames_per_split: int = 10000):
    frame_lines = get_frame_lines(input_file)
    file_idx = 1
    buf = []
    count = 0

    with open(input_file) as f:
        while True:
            frame = [f.readline() for _ in range(frame_lines)]
            if not frame[0]:
                break
            if len(frame) < frame_lines or any(line == "" for line in frame):
                print("Warning: incomplete frame skipped")
                continue
            buf.extend(frame)
            count += 1
            if count >= frames_per_split:
                out = f"split_{file_idx}.xyz"
                with open(out, "w") as o:
                    o.writelines(buf)
                print(f"Wrote {out} ({count} frames)")
                file_idx += 1
                buf, count = [], 0

    if buf:
        out = f"split_{file_idx}.xyz"
        with open(out, "w") as o:
            o.writelines(buf)
        print(f"Wrote {out} ({count} frames)")


def run(input_file: str, frames_per_file: int):
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"{input_file} not found")
    if frames_per_file < 1:
        raise ValueError("frames-per-file must be ≥1")
    split_xyz(input_file, frames_per_file)
