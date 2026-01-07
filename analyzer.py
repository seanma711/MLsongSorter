import librosa
import numpy as np
import json
import os

def analyze_song(filepath):
    # Load audio (sr=None keeps original sample rate, but let's use 22050 for consistency)
    y, sr = librosa.load(filepath, sr=22050)
    
    # Tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    
    # Energy
    rms = librosa.feature.rms(y=y)
    energy = float(np.mean(rms))
    
    # Spectral centroid (brightness)
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    brightness = float(np.mean(centroid))
    
    # Spectral contrast (punchy vs smooth)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    contrast_mean = float(np.mean(contrast))
    
    # Spectral rolloff (where the high frequencies drop off)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    rolloff_mean = float(np.mean(rolloff))
    
    # MFCCs (timbre - 13 coefficients, averaged)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = [float(np.mean(coef)) for coef in mfccs]
    
    # Chroma (pitch classes)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = [float(np.mean(c)) for c in chroma]
    
    # Tonnetz (harmonic relationships)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
    tonnetz_mean = [float(np.mean(t)) for t in tonnetz]
    
    return {
        "tempo": float(tempo),
        "energy": energy,
        "brightness": brightness,
        "contrast": contrast_mean,
        "rolloff": rolloff_mean,
        "mfccs": mfccs_mean,
        "chroma": chroma_mean,
        "tonnetz": tonnetz_mean,
    }


def analyze_all():
    audio_folder = "audio"
    
    # Load song metadata to map IDs to names
    with open('songs.json', 'r') as f:
        songs = json.load(f)
    
    song_lookup = {s['id']: s for s in songs}
    
    results = []
    files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]
    
    for i, filename in enumerate(files):
        spotify_id = filename.replace('.mp3', '')
        filepath = os.path.join(audio_folder, filename)
        
        song_info = song_lookup.get(spotify_id, {})
        print(f"[{i+1}/{len(files)}] Analyzing: {song_info.get('name', spotify_id)}")
        
        try:
            features = analyze_song(filepath)
            features['id'] = spotify_id
            features['name'] = song_info.get('name', '')
            features['artist'] = song_info.get('artist', '')
            results.append(features)
        except Exception as e:
            print(f"  Error: {e}")
    
    # Save results
    with open('features.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDone! Analyzed {len(results)} songs. Saved to features.json")
def analyze_all():
    audio_folder = "audio"
    
    # Load song metadata to map IDs to names
    with open('songs.json', 'r') as f:
        songs = json.load(f)
    
    song_lookup = {s['id']: s for s in songs}
    
    results = []
    files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]
    
    for i, filename in enumerate(files):
        spotify_id = filename.replace('.mp3', '')
        filepath = os.path.join(audio_folder, filename)
        
        song_info = song_lookup.get(spotify_id, {})
        print(f"[{i+1}/{len(files)}] Analyzing: {song_info.get('name', spotify_id)}")
        
        try:
            features = analyze_song(filepath)
            features['id'] = spotify_id
            features['name'] = song_info.get('name', '')
            features['artist'] = song_info.get('artist', '')
            results.append(features)
        except Exception as e:
            print(f"  Error: {e}")
    
    # Save results
    with open('features.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDone! Analyzed {len(results)} songs. Saved to features.json")


if __name__ == "__main__":
    print(analyze_song("audio/0A7lEsDtaJ6jw5r2lGaIhI.mp3"))