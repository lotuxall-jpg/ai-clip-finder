import requests
import re

# 🔹 Put the YouTube video ID here
VIDEO_ID = "dQw4w9WgXcQ"  # replace with real video

def get_transcript(video_id):
    url = f"https://youtubetranscript.com/?server_vid2={video_id}"
    response = requests.get(url)
    return response.text

def find_viral_moments(transcript):
    keywords = ["WHAT", "NO WAY", "BRO", "OH MY GOD", "SCREAM", "YELL"]

    moments = []
    lines = transcript.split("\n")

    for i, line in enumerate(lines):
        for word in keywords:
            if word.lower() in line.lower():
                start = max(0, i - 2)
                end = i + 2
                clip = " ".join(lines[start:end])
                moments.append(clip)

    return moments[:5]

def main():
    transcript = get_transcript(VIDEO_ID)
    moments = find_viral_moments(transcript)

    print("🔥 Viral Moments Found:\n")
    for i, moment in enumerate(moments, 1):
        print(f"{i}. {moment}\n")

if __name__ == "__main__":
    main()
