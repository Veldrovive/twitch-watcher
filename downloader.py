import constants
import memory
import os
import ffmpeg

import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def download (video_id, video_title, m3u8_url, channel_name):
    # Download the video
    create_channel_dir(channel_name)
    video_name = f"{constants.VIDEO_DIRECTORY}/{channel_name}/{slugify(video_title)}.{constants.OUTPUT_FORMAT}"
    (
        ffmpeg
        .input(m3u8_url)
        .trim(start_frame=0, end_frame=120)
        .output(video_name, format=constants.OUTPUT_FORMAT)
        .overwrite_output()
        .run()
    )
    # Add the video id to the json file
    memory.downloaded_video(video_id, video_title, channel_name)

def create_channel_dir (channel_name):
    # Create a subdirectory of constants.MEMORY_DIRECTORY to store the downloaded video ids
    os.makedirs(f"{constants.VIDEO_DIRECTORY}/{channel_name}", exist_ok=True)