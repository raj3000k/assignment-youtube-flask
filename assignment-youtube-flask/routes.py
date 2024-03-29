import requests
from isodate import parse_duration
from dotenv import load_dotenv
import os

from flask import Blueprint, render_template, current_app, request, redirect

main = Blueprint('main', __name__)


load_dotenv()

@main.route('/', methods=['GET', 'POST'])
def index():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    if request.method == 'POST':
        search_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'q' : request.form.get('query'),
            'part' : 'snippet',
            'maxResults' : 8,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.form.get('submit') == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : current_app.config['YOUTUBE_API_KEY'],
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title' : result['snippet']['title'],
            }
            videos.append(video_data)
        
        # Apply filter 
        if request.form.get('filter'):
            filter_criteria = request.form.get('filter')
            videos = filter_videos(videos, filter_criteria)

    return render_template('index.html', videos=videos)

def filter_videos(videos, filter_criteria):
    if filter_criteria == 'date':
        return sorted(videos, key=lambda x: x['published_at'], reverse=True)
    elif filter_criteria == 'views':
        return sorted(videos, key=lambda x: x['views'], reverse=True)
    elif filter_criteria == 'rating':
        return sorted(videos, key=lambda x: x['rating'], reverse=True)
    else:
        return videos

# Youtube API Response
def inspect_youtube_api():
    API_KEY = os.getenv('YOUTUBE_API_KEY')
    search_url = 'https://www.googleapis.com/youtube/v3/search'  # Define search URL

    
    search_params = {
        'key': API_KEY,
        'q': 'cats',  # Example query
        'part': 'snippet',
        'maxResults': 9,  # Get only one result for inspection
        'type': 'video'
    }
    response = requests.get(search_url, params=search_params)

    # If request was successful
    if response.status_code == 200:
        
        data = response.json()
        
        print(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Calling the function to API Response
inspect_youtube_api()
