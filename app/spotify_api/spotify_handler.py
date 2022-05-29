import json
import requests

class SpotifyHandler:
    # Spotify API URLS
    API_VERSION = "v1"
    SPOTIFY_API_BASE_URL = "https://api.spotify.com"
    SPOTIFY_API_URL = f"{SPOTIFY_API_BASE_URL}/{API_VERSION}"

    #for user's basic information
    def get_user_profile_data(self, auth_header):
        user_profile_api_endpoint = f"{self.SPOTIFY_API_URL}/me"
        profile_data = requests.get(user_profile_api_endpoint, headers=auth_header).text
        return json.loads(profile_data)

    
        
    #for song's information
    def get_img_and_url(self,auth_header,song):
        query=f'{song}'
        search_track_endpoint= f"https://api.spotify.com/v1/search?q={query}&type=track"
        track=json.loads(requests.get(search_track_endpoint, headers=auth_header).text)
        track_items=[]
        track_items.append({
            'track_img':track['tracks']['items'][0]['album']['images'][0]['url'],
            'track_id':track['tracks']['items'][0]['album']['id'],
            'track_url':track['tracks']['items'][0]['external_urls']['spotify'],
            'track_name':track['tracks']['items'][0]['name']
        })

        return track_items
 
    