import yt_dlp
import os
import json
import time

def download_song(name, artist, spotify_id, duration_ms, output_folder="audio"):
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
            # Search without downloading first
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            video = info['entries'][0]
            
            # Check duration (10% tolerance)
            expected_sec = duration_ms / 1000
            actual_sec = video['duration']
            diff_percent = abs(expected_sec - actual_sec) / expected_sec
            
            if diff_percent > 0.10:
                print(f"Duration mismatch: {name} - {artist} (expected {expected_sec:.0f}s, got {actual_sec}s)")
                return {"status": "duration_mismatch", "id": spotify_id, "expected": expected_sec, "actual": actual_sec}
            
            # Download if checks pass
            ydl.download([video['webpage_url']])
            print(f"Downloaded: {name} - {artist}")
            return {"status": "success", "id": spotify_id}
            
    except Exception as e:
        print(f"Failed: {name} - {artist} - {e}")
        return {"status": "failed", "id": spotify_id, "error": str(e)}


if __name__ == "__main__":
    # Test with one song from your library
    download_song("Chamber Of Reflection", "Mac DeMarco", "test123", 323000)