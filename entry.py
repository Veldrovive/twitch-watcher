import constants
import requests
import json
import memory
import downloader
import time

def get_past_video_map (channel_name):
    body = [
        {
            "operationName": "ChannelVideoShelvesQuery",
            "variables": {
                "channelLogin": channel_name,
                "first": constants.LOOKBACK_NUM
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": constants.PERSISTED_QUERY_HASH
                }
            }
        }
    ]
    body = json.dumps(body)
    headers = {
        "Client-ID": constants.CLIENT_ID,
        "Content-Type": "application/json"
    }
    r = requests.post(constants.GQL_ENDPOINT, data=body, headers=headers)
    r.raise_for_status()
    data = r.json()

    edges = data[0]["data"]["user"]["videoShelves"]["edges"]

    recent_video_node = None
    for edge in edges:
        if edge["node"]["type"] == "LATEST_BROADCASTS":
            recent_video_node = edge["node"]["items"]
            break
    if recent_video_node is None:
        raise Exception("Could not find recent broadcasts")

    video_map = {}
    for video in recent_video_node[0:constants.LOOKBACK_NUM]:
        preview_url = video["animatedPreviewURL"]
        url_parts = preview_url.split("/")
        # Find the url part that contains storyboards
        base_url = "/".join(url_parts[0:url_parts.index("storyboards")])
        m3u8_url = base_url + "/chunked/index-dvr.m3u8"
        video_map[video["id"]] = { "title": video["title"], "m3u8_url": m3u8_url }
    return video_map

def download_past_videos (channel_name):
    video_map = get_past_video_map(channel_name)
    to_download = memory.get_not_downloaded(list(video_map.keys()), channel_name)
    for video_id in to_download:
        m3u8_url = video_map[video_id]["m3u8_url"]
        video_title = video_map[video_id]["title"]
        print("Video id:", video_id, "has not been downloaded yet. Downloading...", channel_name, video_title)
        downloader.download(video_id, video_title, m3u8_url, channel_name)

def watch_channels (channel_names):
    # Downloads the last few video for each channel. Checks again every PING_INTERVAL seconds
    while True:
        for channel_name in channel_names:
            print("Checking channel:", channel_name)
            try:
                download_past_videos(channel_name)
            except Exception as e:
                print("Error downloading past videos for channel:", channel_name, e)
        print("Sleeping for", constants.PING_INTERVAL, "seconds...")
        time.sleep(constants.PING_INTERVAL)
        

if __name__ == "__main__":
    # print(get_past_video_map("criticalrole"))
    # download_past_videos("criticalrole")
    watch_channels([
        'criticalrole',
        'secretsleepoversociety'
    ])