from datetime import datetime
from fastapi import HTTPException
import requests

class SpotifyService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def notify_playback(self, track_uri: str, play_time: str):
        spotify_url = f"{self.base_url}/schedule-playlist"
        
        params = {
            "playlist_uri": track_uri,
            "play_time": datetime.strptime(play_time, "%Y-%m-%dT%H:%M:%S%z").strftime("%H:%M")
        }

        try:
            response = requests.get(spotify_url, params=params)
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to schedule Spotify playback")

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error scheduling Spotify playback")