import matplotlib.pyplot as plt
import os
import cv2


# Load a video file and return the capture object
def load_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception("Error: Cannot open video file.")
    return cap


# Extract and save the first frame as PNG
def display_first_frame(video_path, save_path="first_frame.png"):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.imshow(frame_rgb)
        plt.title("First Frame")
        plt.axis("off")
        plt.savefig(save_path)
        plt.show()
    else:
        raise Exception("Error: Failed to read the first frame.")


# Read video properties: resolution, fps and frame count
def get_video_properties(cap):
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Resolution: {width}x{height}")
    print(f"Total frames: {total_frames}")
    print(f"FPS: {fps}")
    return width, height, fps, total_frames


# Extract and save a short segment (e.g. 5 seconds)
def extract_segment(input_path, output_path, duration, fps, width, height):
    cap = cv2.VideoCapture(input_path)
    segment_frames = duration * fps
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    count = 0
    while count < segment_frames:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        count += 1

    cap.release()
    out.release()


# Convert video to grayscale
def convert_to_grayscale(input_path, output_path, fps, width, height):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gray)

    cap.release()
    out.release()


# Resize video by scaling resolution (e.g. half size)
def resize_video(input_path, output_path, fps, width, height, scale=0.5):
    cap = cv2.VideoCapture(input_path)
    new_width = int(width * scale)
    new_height = int(height * scale)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        resized = cv2.resize(frame, (new_width, new_height))
        out.write(resized)

    cap.release()
    out.release()


# Compress video using MJPG codec and save as .avi
def compress_video(input_path, output_path, fps, width, height):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()


# Print size of files in MB
def compare_file_sizes(*paths):
    for path in paths:
        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"{path}: {size_mb:.2f} MB")


def main():
    video_path = "input.mp4"
    segment_path = "segment_video.mp4"
    gray_path = "gray_video.mp4"
    resized_segment_path = "resized_segment.mp4"
    compressed_segment_path = "compressed_segment.avi"

    # Load and read properties
    cap = load_video(video_path)
    display_first_frame(video_path)
    width, height, fps, total_frames = get_video_properties(cap)
    cap.release()

    # Segment extraction
    extract_segment(video_path, segment_path, duration=5, fps=fps, width=width, height=height)

    # Grayscale conversion of segment
    convert_to_grayscale(segment_path, gray_path, fps=fps, width=width, height=height)

    # Resize of segment
    resize_video(segment_path, resized_segment_path, fps=fps, width=width, height=height, scale=0.5)

    # Compression of segment
    compress_video(segment_path, compressed_segment_path, fps=fps, width=width, height=height)

    # Compare all output sizes
    compare_file_sizes(
        segment_path,
        gray_path,
        resized_segment_path,
        compressed_segment_path,
    )


if __name__ == "__main__":
    main()
