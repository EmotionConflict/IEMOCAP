import os 
import pandas as pd
import shutil




base_path = "/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video"
# "/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/Session1_Video"
# audio_des_path = os.path.join(base_path,"output_qwen_description1")
# video_des_path = os.path.join(base_path,"openai_test_subset_peak_frame_description")
# text_des_path = os.path.join(base_path,"Session1_Text")
video_des_path = os.path.join(base_path,"Session1_Video")

# os.makedirs(os.path.join(base_path,"sample20peremotion"),exist_ok=True)
# os.makedirs(os.path.join(base_path,"sample20peremotion","audio"),exist_ok=True)
os.makedirs(os.path.join(base_path,"sample20peremotion","video_raw"),exist_ok=True)
# os.makedirs(os.path.join(base_path,"sample20peremotion","text"),exist_ok=True)
# os.makedirs(os.path.join(base_path,"sample20peremotion","au"),exist_ok=True)


df = pd.read_csv("/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/sample20peremotion/available_samples_20_per_emotion.csv")



        


rows_all = []

for _, row in df.iterrows():
    file_name = row["File_Name"]
    video_path = os.path.join(video_des_path, f"{file_name}.mp4")
    # audio_path = os.path.join(audio_des_path, f"{file_name}.txt")
    # text_path  = os.path.join(text_des_path,  f"{file_name}.txt")
    # au_path    = os.path.join(au_des_path,    f"{file_name}.csv")

    # if all(os.path.exists(p) for p in [video_path, audio_path, text_path, au_path]):
    # print(f"Copying {file_name} descriptions")
    # rows_all.append(row.to_dict())

    shutil.copy(video_path, os.path.join(base_path, "sample20peremotion", "video_raw", f"{file_name}.mp4"))
        # shutil.copy(audio_path, os.path.join(base_path, "sample20peremotion", "audio", f"{file_name}.txt"))
        # shutil.copy(text_path,  os.path.join(base_path, "sample20peremotion", "text",  f"{file_name}.txt"))
        # shutil.copy(au_path,    os.path.join(base_path, "sample20peremotion", "au",    f"{file_name}.csv"))

# Create and save filtered DataFrame
# df_all = pd.DataFrame(rows_all)
# df_all.to_csv(os.path.join(base_path, "sample20peremotion", "available_videos_20_per_emotion.csv"), index=False)





    #extract descriptions 

