import time
from transcript_generator import generate_transcript
from transcript_analyzer import analyze_transcript

# Is This Game Better Than Minecraft? (Hytale) - DanTDM
# https://www.youtube.com/watch?v=Qq_EZZxmdyw

# level 16 xbow is terrifying - Ken
# https://www.youtube.com/watch?v=1YZDN5ANsJs

#Sidemen Silent Library
# https://www.youtube.com/watch?v=G9b7clmSd4g

def main():
    video_id = "G9b7clmSd4g"
    generate_transcript(video_id)
    analyze_transcript()

if __name__ == "__main__":
    main()
    