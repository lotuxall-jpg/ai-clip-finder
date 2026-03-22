import os
import requests
import random
from pytube import YouTube
from moviepy.editor import VideoFileClip

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def send_video(file):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVideo"
    with open(file, "rb") as vid:
        requests.post(url, data={"chat_id": CHAT_ID}, files={"video": vid})

def get_video(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=1"
    data = requests.get(url).json()
    try:
        vid = data["items"][0]["id"]["videoId"]
        return f"https://youtube.com/watch?v={vid}"
    except:
        return None

def download(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
        stream.download(filename="video.mp4")
        return "video.mp4"
    except:
        return None

def make_clips(video):
    clips = []
    vid = VideoFileClip(video)
    duration = int(vid.duration)

    for i in range(2):
        start = random.randint(0, max(1, duration - 40))
        end = start + 25
        clip = vid.subclip(start, end)
        name = f"clip{i}.mp4"
        clip.write_videofile(name, codec="libx264", audio_codec="aac")
        clips.append(name)

    return clips

def main():
    channels = [
        "UCWsDFcIhY2DBi3GB5uykGXA",  # IShowSpeed
        "UC9gFih9rw0zNCK3ZtoKQQyA",  # Kai Cenat
        "UCVtFOytbRpEvzLjvqGG5gxQ",  # Jynxzi
        "UC4ncvgh5hFr5O83MH7-jRJg"   # Joe Bartolozzi
    ]

    send_message("🔍 Finding video...")

    url = get_video(random.choice(channels))

    if not url:
        send_message("❌ No video found")
        return

    send_message(f"🎬 {url}")

    vid = download(url)

    if not vid:
        send_message("❌ Download failed")
        return

    send_message("✂️ Making clips...")

    clips = make_clips(vid)

    for c in clips:
        send_video(c)

    send_message("✅ Done!")

if __name__ == "__main__":
    main()
