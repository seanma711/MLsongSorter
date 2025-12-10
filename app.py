from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_sp_oauth():
    print(os.getenv("SPOTIPY_REDIRECT_URI"))
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-library-read playlist-modify-public playlist-modify-private",
        open_browser=False,
    )

def get_spotify_client():
    sp_oauth = get_sp_oauth()
    if token_info := sp_oauth.get_cached_token():
        return spotipy.Spotify(auth=token_info['access_token'])
    else:
        return None

@app.route("/callback")
def callback():
    code = request.args.get('code')
    sp_oauth = get_sp_oauth()
    sp_oauth.get_access_token(code)
    return "Logged in successfully! You can close this window."

@app.route("/login")
def login():
    sp_oauth = get_sp_oauth()
    token_info = sp_oauth.get_cached_token()
    
    if token_info:
        return jsonify({"message": "Already logged in"})
    
    return redirect(sp_oauth.get_authorize_url())

@app.route("/fetch_liked_songs")
def fetch_liked_songs():
    sp = get_spotify_client()
    if not sp:
        return redirect("/login")

    results = sp.current_user_saved_tracks(limit=50)
    songs = []
    for item in results['items']:
        track = item['track']
        features = sp.audio_features(track['id'])[0]
        songs.append({
            "id": track['id'],
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "energy": features['energy'],
            "danceability": features['danceability'],
            "valence": features['valence'],
            "acousticness": features['acousticness'],
            "tempo": features['tempo'],
            "instrumentalness": features['instrumentalness']
        })

    return jsonify(songs)

if __name__ == "__main__":
    app.run(debug=True, port=8000)