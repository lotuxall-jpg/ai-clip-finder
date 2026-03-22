import requests
import xml.etree.ElementTree as ET

# 🔹 Put channel ID here (Kai Cenat example)
CHANNEL_ID = "UC4x5xZx9PpZ2fQnYz0g1gYw"  # replace later

def get_latest_video(channel_id):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    response = requests.get(url)
    root = ET.fromstring(response.content)

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text
        return video_id

def get_transcript(video_id):
    url = f"https://youtubetranscript.com/?server_vid2={video_id}"
    response = requests.get(url)
    return response.text

def find_viral_moments(transcript):
    keywords = ["WHAT", "NO WAY", "BRO", "OH MY GOD", "SCREAM", "YELL"]
    lines = transcript.split("\n")

    moments = []

    for i, line in enumerate(lines):
        for word in keywords:
            if word.lower() in line.lower():
                start = max(0, i - 2)
                end = i + 2
                clip = " ".join(lines[start:end])
                moments.append(clip)

    return moments[:5]

def main():
    video_id = get_latest_video(CHANNEL_ID)
    print(f"🎥 Latest Video ID: {video_id}")

    transcript = get_transcript(video_id)
    moments = find_viral_moments(transcript)

    print("\n🔥 Viral Moments:\n")
    for i, moment in enumerate(moments, 1):
        print(f"{i}. {moment}\n")

if __name__ == "__main__":
    main()
