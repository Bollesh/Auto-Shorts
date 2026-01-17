import json
from youtube_transcript_api import YouTubeTranscriptApi

def generate_transcript(video_id: str):
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)
    
    with open("transcript/transcript.json", "w") as f:
        json.dump(fetched_transcript.to_raw_data(), f, indent=4)
    print("Transcript generated")
