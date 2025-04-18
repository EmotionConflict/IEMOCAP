import subprocess
import json

video_path = "/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/utterance_videos/Session1/Ses01M_impro06_F000.avi"

# def get_video_duration_ffmpeg(video_path):
#     cmd = [
#         "ffprobe",
#         "-v", "error",
#         "-show_entries", "format=duration",
#         "-of", "json",
#         video_path
#     ]
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     output = json.loads(result.stdout)
#     return float(output["format"]["duration"])

# # Example
# print(get_video_duration_ffmpeg(video_path ))










import cv2

def get_video_duration_opencv(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Could not open video: {video_path}")
        return None
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps if fps > 0 else None
    cap.release()
    return duration

# Example

print(f"⏱ Duration: {get_video_duration_opencv(video_path):.2f} seconds")