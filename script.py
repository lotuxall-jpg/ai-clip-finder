import requests
import xml.etree.ElementTree as ET
from youtube_transcript_api import YouTubeTranscriptApi
import subprocess
import os

# 🔹 TELEGRAM INFO
TELEGRAM_TOKEN = "8699414099:AAGA89Ig1Ijwn0gzWQM0jlfE1bYUi6L5970"
CHAT_ID = "8205944221"

# 🔥 CHANNELS
CHANNELS = {
    "Kai Cenat": "UCvC4D8onUfXzvjTOM-dBfEA",
    "IShowSpeed": "UCWsDFcIhY2DBi3GB5uykGXA"
}

# 🔍 GET LATEST VIDEO
def get_latest_video(channel_id):
    try:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        response = requests.get(url)
        root = ET.fromstring(response.content)

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text
            return video_id
    except:
        return None

# 📜 GET TRANSCRIPT
def get_transcript(video_id):
    try:
        return YouTubeTranscriptApi.get_transcript(video_id)
    except:
        return []

# 🔥 FIND MOMENTS
def find_moments(transcript):
    keywords = [
        "no way", "oh my god", "bro", "what", "this is crazy",
        "ain't no way", "nah", "yo", "chat", "wtf",
        "that's insane", "i can't believe"
    ]

    timestamps = []

    for entry in transcript:
        text = entry["text"].lower()
        start = int(entry["start"])

        if any(word in text for word in keywords):
            timestamps.append(start)

    return timestamps[:2]

# 🎥 DOWNLOAD VIDEO
def download_video(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"

    subprocess.run([
        "yt-dlp",
        "-f", "mp4",
        "-o", "video.mp4",
        url
    ])

    return "video.mp4"

# ✂️ CUT CLIP
def cut_clip(start, duration=20):
    output = f"clip_{start}.mp4"

    subprocess.run([
        "ffmpeg",
        "-ss", str(start),
        "-i", "video.mp4",
        "-t", str(duration),
        "-c", "copy",
        output
    ])

    return output

# 📲 SEND VIDEO
def send_video(file_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"

    with open(file_path, "rb") as video:
        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": caption
            },
            files={"video": video}
        )

# 🚀 MAIN
def main():
    for name, channel_id in CHANNELS.items():
        video_id = get_latest_video(channel_id)

        if not video_id:
            continue

        transcript = get_transcript(video_id)

        if not transcript:
            continue

        timestamps = find_moments(transcript)

        if not timestamps:
            continue

        video_file = download_video(video_id)

        for t in timestamps:
            clip = cut_clip(t)

            minutes = t // 60
            seconds = t % 60

            caption = f"🔥 {name} | {minutes:02d}:{seconds:02d}"

            send_video(clip, caption)

        # 🧹 CLEAN FILES
        for file in os.listdir():
            if file.endswith(".mp4"):
                os.remove(file)


if __name__ == "__main__":
    main()
