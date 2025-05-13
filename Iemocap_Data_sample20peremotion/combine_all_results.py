import os
import json
import csv

# Input and output file paths
base_apth = '/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/sample20peremotion'
input_path = os.path.join(base_apth, 'au_results.json')
# '/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/xxx_session1/all_descriptions/au_results.json'
output_path = os.path.join(base_apth, 'iemocap_20sample_annotations.json')
# '/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/common/iemocap_final_annotations.json'
audio_desc_dir = os.path.join(base_apth, 'audio')
# '/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/common/output_qwen_description_colab_common'
visual_obj_desc_dir = os.path.join(base_apth, 'video')
# '/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/common/openai_test_subset_peak_frame_description'
# '/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/common/openai_test_subset_peak_frame_description'
caption_dir = os.path.join(base_apth, 'text')
# '/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/common/Session1_Text'
# '/Users/summerghorbani/Documents/MIT_projects/How2AI/IEMOCAP_full_release/test_video/common/Session1_Text_common'

def get_audio_description(sample_id):
    txt_file = os.path.join(audio_desc_dir, f'{sample_id}.txt')
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            return f.read().strip()
    return ''

def get_visual_objective_description(sample_id):
    csv_file = os.path.join(visual_obj_desc_dir, f'{sample_id}.csv')
    if os.path.exists(csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                return row.get('description', '').strip()
    return ''

def get_caption(sample_id):
    txt_file = os.path.join(caption_dir, f'{sample_id}.txt')
    if os.path.exists(txt_file):
        with open(txt_file, 'r') as f:
            return f.read().strip()
    return ''

def convert_first_step_to_final_annotations(input_path, output_path):
    with open(input_path, 'r') as infile:
        data = json.load(infile)

    output = []
    for sample_id, sample in data.items():
        entry = {
            'video_id': f'{sample_id}.mp4',
            'peak_time': sample.get('peak_time', 0.0),
            'visual_expression_description': sample.get('au_phrases', []),
            'visual_objective_description': get_visual_objective_description(sample_id),
            'raw_AU_values_at_peak': sample.get('au_data', {}),
            'coarse-grained_summary': '',
            'fine-grained_summary': '',
            'audio_description': get_audio_description(sample_id),
            'caption': get_caption(sample_id)
        }
        output.append(entry)

    with open(output_path, 'w') as outfile:
        json.dump(output, outfile, indent=4, ensure_ascii=False)



def add_discrete_emotion_to_annotations(json_path, csv_path, output_path=None):
    # Build mapping from sample name to Emotion, excluding 'xxx'
    label_map = {}
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # if row['Emotion'].strip().lower() != 'xxx':
                name = row['File_Name'] + '.mp4'
                label_map[name] = row['Emotion']

    # Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Update or filter objects based on label_map
    updated_data = []
    for obj in data:
        vid = obj.get('video_id')
        if vid in label_map:
            obj['Emotion'] = label_map[vid]
            updated_data.append(obj)
        else:
            # Skip entries with missing or 'xxx' labels
            continue

    # Write back (optionally to a new file)
    out_path = output_path if output_path else json_path
    with open(out_path, 'w') as f:
        json.dump(updated_data, f, indent=4, ensure_ascii=False)







if __name__ == '__main__':
    convert_first_step_to_final_annotations(input_path, output_path)
    # Uncomment the following line to run the update
    # add_discrete_and_valence_to_annotations
    add_discrete_emotion_to_annotations(
        output_path,
        os.path.join(base_apth,'sample_20_per_emotion.csv' ),
        os.path.join(base_apth,'iemocap_final_annotations_with_emotion.json')  # Optional: specify a different output path if needed
    )
    pass
