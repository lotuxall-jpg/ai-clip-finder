import requests
import os
import random
from moviepy.editor import VideoFileClip
import yt_dlp

# =========================
# 🔑 PUT YOUR INFO HERE
# =========================
BOT_TOKEN = "8699414099:AAGA89Ig1Ijwn0gzWQM0jlfE1bYUi6L5970"
CHAT_ID = "8205944221"
YOUTUBE_API_KEY = "AIzaSyBtVTfIH_C-ebrQOZha_37CyfugyyAfJ-8"

# Channels (IShowSpeed, Kai Cenat, Jynxzi, Joe Bartolozzi)
CHANNEL_IDS = [
    "UCWsDFcIhY2DBi3GB5uykGXA",  # IShowSpeed
    "UC8m8c-6Yz9b0c2Y0l8kX1hA",  # Kai Cenat (example)
    "UC9x4x2Z8W5y5Gg8cJ1fKJ2Q",  # Jynxzi (example)
    "UCv0hP5x0YwF5c6M0B8j0g8g"   # Joe Bartolozzi (example)
]

# =========================
# 📲 TELEGRAM SEND
# =========================
def send_video(file_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo"
    with open(file_path, "rb") as video:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"video": video})

# =========================
# 🎥 GET RANDOM VIDEO
# =========================
def get_video():
    channel_id = random.choice(CHANNEL_IDS)

    url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=5"
    data = requests.get(url).json()

    for item in data["items"]:
        if item["id"]["kind"] == "youtube#video":
            return item["id"]["videoId"]

# =========================
# ⬇️ DOWNLOAD VIDEO
# =========================
def download_video(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "best",
        "outtmpl": "video.mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "video.mp4"

# =========================
# ✂️ CREATE CLIP
# =========================
def make_clip(input_file):
    clip = VideoFileClip(input_file)

    duration = clip.duration

    # pick random 20–40 sec clip
    start = random.randint(0, int(duration - 40))
    end = start + random.randint(20, 40)

    final = clip.subclip(start, end)
    output = "clip.mp4"
    final.write_videofile(output, codec="libx264", audio_codec="aac")

    return output, start

# =========================
# 🚀 MAIN
# =========================
def main():
    video_id = get_video()

    if not video_id:
        print("No video found")
        return

    print("Downloading video...")
    video_file = download_video(video_id)

    print("Creating clip...")
    clip_file, start_time = make_clip(video_file)

    video_link = f"https://youtu.be/{video_id}?t={start_time}"

    caption = f"🔥 Viral Clip\n\n🎥 Watch full: {video_link}"

    print("Sending to Telegram...")
    send_video(clip_file, caption)

if __name__ == "__main__":
    main()
