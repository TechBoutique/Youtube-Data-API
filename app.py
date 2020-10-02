import requests  
from flask import Flask   
from flask import render_template   
from flask import url_for
from isodate import parse_duration   
from flask import request

# YOUTUBE_API_KEY =os.environ.get('YOUTUBE_API_KEY')

key = 'AIzaSyDYk-aoMoquYXlIfpyl-RXsdZC6iVFcdnI'


app = Flask(__name__)      


@app.route('/', methods = ['GET', 'POST'])    
def mainpage():  
    search_url = 'https://www.googleapis.com/youtube/v3/search'       
    video_url = 'https://www.googleapis.com/youtube/v3/videos'       
    videos = []
    if request.method == 'POST':
        search_query=request.form.get('query')   
        print(search_query)
        search_term = {   
                'key' : key,   
                'q'  : request.form.get('query'),    
                'part' : 'snippet',  
                'maxResults' : 18, 
                'order' : 'viewCount',   
                'type' : 'video'  
            }

        r = requests.get(search_url , params = search_term)   

        # print(r.json()[['items']])  
        results = r.json()['items']   
        
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])   
            
        videos = []  

        video_term = {
                'key' : key,
                'id' : ','.join(video_ids),
                'part' : 'snippet,contentDetails',
                'maxResults' : 18
            }   
        r = requests.get(video_url, params=video_term)
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



    return render_template('home.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
