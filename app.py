import yt_dlp
import os

def download_song(name, artist, spotify_id, output_folder="audio"):
    output_path = f"{output_folder}/{spotify_id}"
    
    # Skip if already downloaded
    if os.path.exists(f"{output_path}.mp3"):
        print(f"Already have: {name} - {artist}")
        return {"status": "skipped", "id": spotify_id}
    
    query = f"{name} {artist} audio"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch1:{query}"])
        print(f"Downloaded: {name} - {artist}")
        return {"status": "success", "id": spotify_id}
            
    except Exception as e:
        print(f"Failed: {name} - {artist} - {e}")
        return {"status": "failed", "id": spotify_id, "error": str(e)}


if __name__ == "__main__":
    download_song("Chamber Of Reflection", "Mac DeMarco", "test123")