import constants
import json
import os

def downloaded_video (video_id, video_name, channel_name):
    # Add the video id to the json file
    data = get_channel_data(channel_name)
    data[video_id] = video_name
    write_channel_data(channel_name, data)

def is_downloaded (video_ids, channel_name):
    # Create an object of key=video_id, value=is_downloaded
    video_map = {}
    data = get_channel_data(channel_name)
    for video_id in video_ids:
        video_map[video_id] = video_id in data
    return video_map

def get_not_downloaded (video_ids, channel_name):
    # Returns an array of video_ids that are not downloaded
    video_map = is_downloaded(video_ids, channel_name)
    return [video_id for video_id in video_ids if not video_map[video_id]]

def create_memory_dir ():
    # Create a directory to store the downloaded video ids
    os.makedirs(constants.MEMORY_DIRECTORY, exist_ok=True)

def create_channel (channel_name):
    # Create a json file to store the downloaded video ids
    with open(f"{constants.MEMORY_DIRECTORY}/{channel_name}.json", "w") as f:
        json.dump({}, f)

def safe_init_channel (channel_name):
    # Calls create_memory_dir if the directory does not exist and create_channel if the json file does not exist
    if not os.path.exists(constants.MEMORY_DIRECTORY):
        create_memory_dir()
    if not os.path.exists(f"{constants.MEMORY_DIRECTORY}/{channel_name}.json"):
        create_channel(channel_name)

def get_channel_data (channel_name):
    # Get the downloaded video ids from the json file
    safe_init_channel(channel_name)
    with open(f"{constants.MEMORY_DIRECTORY}/{channel_name}.json", "r") as f:
        data = json.load(f)
    return data

def write_channel_data (channel_name, data):
    # Write the downloaded video ids to the json file
    safe_init_channel(channel_name)
    with open(f"{constants.MEMORY_DIRECTORY}/{channel_name}.json", "w") as f:
        json.dump(data, f)
