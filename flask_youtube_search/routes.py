import requests
from isodate import parse_duration
from flask import Blueprint, render_template, current_app, request, redirect
import random

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    videos = []

    if request.method == 'POST':

        search_params = {
            'key': current_app.config['YOUTUBE_API_KEY'],
            'q': request.form.get('query'),
            'part': 'snippet',
            'maxResults': 12,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)

        video_ids = []
        results = r.json()['items']

        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.form.get('submit') == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[random.randrange(0, len(video_ids) -1)]}')

        video_params = {
            'key': current_app.config['YOUTUBE_API_KEY'],
            'id': ','.join(video_ids),
            'part': 'snippet,contentDetails',
            'maxResults': 12,
            'type': 'video'
        }

        r = requests.get(video_url, params=video_params)

        results = r.json()['items']

        for result in results:
            video_data = {
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
                'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title': result['snippet']['title']
            }
            videos.append(video_data)

    return render_template('index.html', videos=videos)
