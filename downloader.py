import yt_dlp
import os
import json
import time

def download_song(name, artist, spotify_id, output_folder="audio"):
    output_path = f"{output_folder}/{spotify_id}"
    
    if os.path.exists(f"{output_path}.mp3"):
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
        return {"status": "success", "id": spotify_id}
    except Exception as e:
        return {"status": "failed", "id": spotify_id, "error": str(e)}


def download_all():
    # Load songs
    with open('songs.json', 'r') as f:
        songs = json.load(f)
    
    # Create audio folder
    os.makedirs('audio', exist_ok=True)
    
    # Track results
    results = {"success": 0, "skipped": 0, "failed": []}
    
    for i, song in enumerate(songs):
        print(f"[{i+1}/{len(songs)}] {song['name']} - {song['artist']}")
        
        result = download_song(song['name'], song['artist'], song['id'])
        
        if result['status'] == 'success':
            results['success'] += 1
        elif result['status'] == 'skipped':
            results['skipped'] += 1
        else:
            results['failed'].append(song)
        
        # Small delay between downloads
        time.sleep(2)
    
    # Save failed songs for retry
    with open('failed.json', 'w') as f:
        json.dump(results['failed'], f, indent=2)
    
    print(f"\nDone! Success: {results['success']}, Skipped: {results['skipped']}, Failed: {len(results['failed'])}")


if __name__ == "__main__":
    download_all()