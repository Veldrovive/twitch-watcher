"""
The docker container calls this script to start downloading videos.
The channels to watch are passed in with the environment variable CHANNELS which is a comma separated list.
"""

import os
import entry
import constants

if __name__ == "__main__":
    # So these constants aren't actually all that constant. Fight me
    # If an environment varibale with the same name as a constant is set, use that instead
    if os.environ.get("PING_INTERVAL") is not None:
        constants.PING_INTERVAL = int(os.environ.get("PING_INTERVAL"))
    if os.environ.get("MEMORY_DIRECTORY") is not None:
        constants.MEMORY_DIRECTORY = os.environ.get("MEMORY_DIRECTORY")
    if os.environ.get("VIDEO_DIRECTORY") is not None:
        constants.VIDEO_DIRECTORY = os.environ.get("VIDEO_DIRECTORY")
    if os.environ.get("OUTPUT_FORMAT") is not None:
        constants.OUTPUT_FORMAT = os.environ.get("OUTPUT_FORMAT")
    if os.environ.get("LOOKBACK_NUM") is not None:
        constants.LOOKBACK_NUM = int(os.environ.get("LOOKBACK_NUM"))

    channels = os.environ.get("CHANNELS").split(",")
    # channels = ['criticalrole']
    # Trim all channels
    channels = [channel.strip() for channel in channels]
    # Start watching the channels
    entry.watch_channels(channels)