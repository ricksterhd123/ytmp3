import json
import requests

def getYoutubeVideoFromKeyword(youtube_api_key, keyword):
    if not keyword:
        return False

    r = requests.get('https://www.googleapis.com/youtube/v3/search', {
        'part': 'snippet',
        'key': youtube_api_key,
        'q': keyword
    })

    r.raise_for_status()
    videos = json.loads(r.text).get('items', None)

    if len(videos) <= 0:
        return False

    first_video = videos[0]
    video_id = first_video.get('id', {}).get('videoId', None)

    if not video_id:
        return False

    return f'https://www.youtube.com/watch?v={video_id}'
