import os
import ffmpeg
from pathlib import Path
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed


 # === Helper: Convert time from 10ms to seconds ===
def convert_10ms_to_sec(t):
        try:
            return float(t) 
        except ValueError:
            print(f" Invalid time value: {t}")
            return None

    # === Clip extraction worker ===
def extract_clip(task):
        utt_id, start, duration, video_path, out_path, session_name = task
        try:
            if not os.path.exists(video_path):
                return f" Video not found for {utt_id}"
            if duration <= 0:
                return f" Skipping {utt_id}: invalid duration ({duration:.2f}s)"

            ffmpeg.input(video_path, ss=start) \
                .output(out_path, t=duration, vcodec='libx264', acodec='aac') \
                .run(quiet=True)
            return f"Extracted {utt_id} ({duration:.2f}s) from {session_name}"
        except ffmpeg.Error as e:
            return f" ffmpeg failed for {utt_id}: {e.stderr.decode() if e.stderr else e}"



def main():
    
    # === Base Configuration ===
    BASE_DIR = "/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release"
    OUT_BASE_DIR = os.path.join(BASE_DIR, "utterance_videos")

   

    # === Process Sessions 1 to 5 ===
    for session_id in range(1, 6):
        session_name = f"Session{session_id}"
        VIDEO_DIR = os.path.join(BASE_DIR, session_name, "dialog", "avi", "DivX")
        LAB_DIR = os.path.join(BASE_DIR, session_name, "dialog", "lab")
        OUT_DIR = os.path.join(OUT_BASE_DIR, session_name)
        os.makedirs(OUT_DIR, exist_ok=True)

        print(f"\n Processing {session_name}...")
        lab_files = list(Path(LAB_DIR).rglob("*.lab"))
        clip_tasks = []

        for lab_path in lab_files:
            lab_path = str(lab_path)
            lab_file = os.path.basename(lab_path)
            video_basename = os.path.splitext(lab_file)[0] + ".avi"
            video_path = os.path.join(VIDEO_DIR, video_basename)

            if not os.path.exists(video_path):
                print(f" Video file not found: {video_path}")
                continue

            try:
                df = pd.read_csv(lab_path, sep='\s+', engine='python', header=None, names=["start", "end", "utt_id"])
                df = df.dropna()
                # df = df[df["start"].apply(lambda x: isinstance(x, (int, float, np.integer, np.floating)) or str(x).replace('.', '', 1).isdigit())]
                # df = df[df["end"].apply(lambda x: isinstance(x, (int, float, np.integer, np.floating)) or str(x).replace('.', '', 1).isdigit())]
            except Exception as e:
                print(f" Failed to load or clean lab file {lab_path}: {e}")
                continue

            for _, row in df.iterrows():
                start = convert_10ms_to_sec(row["start"])
                end = convert_10ms_to_sec(row["end"])
                utt_id = row["utt_id"]

                if start is None or end is None or end <= start:
                    continue

                duration = end - start
                # if duration < 0.5:
                #     continue

                out_path = os.path.join(OUT_DIR, f"{utt_id}.avi")
                clip_tasks.append((utt_id, start, duration, video_path, out_path, session_name))

        print(f" Launching parallel extraction for {len(clip_tasks)} clips in {session_name}...")
        with ProcessPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(extract_clip, task) for task in clip_tasks]
            for future in as_completed(futures):
                print(future.result())


if __name__ == '__main__':
    main()
    print("\n All utterance video clips extracted for all sessions.")
