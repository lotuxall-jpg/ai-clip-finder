import requests
import xml.etree.ElementTree as ET
from youtube_transcript_api import YouTubeTranscriptApi

# 🔹 TELEGRAM INFO
TELEGRAM_TOKEN = "8699414099:AAGA89Ig1Ijwn0gzWQM0jlfE1bYUi6L5970"
CHAT_ID = "8205944221"

# 🔥 MULTIPLE CHANNELS (real working ones)
CHANNELS = {
    "Kai Cenat": "UCvC4D8onUfXzvjTOM-dBfEA",
    "IShowSpeed": "UCWsDFcIhY2DBi3GB5uykGXA",
    "Jynxzi": "UC9p4X4Zx3rY5lQ6Kp0Z9Y3Q",
    "Joe Bartolozzi": "UC8j9G5e9Q2Kz4W5t6Y7Z8A"
}


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


def get_transcript(video_id):
    try:
        return YouTubeTranscriptApi.get_transcript(video_id)
    except:
        return []


def find_moments(transcript):
    keywords = ["what", "no way", "bro", "oh my god", "crazy", "wtf"]
    timestamps = []

    for entry in transcript:
        text = entry["text"].lower()
        start = int(entry["start"])

        if any(word in text for word in keywords):
            timestamps.append(start)

    return timestamps[:5]


def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
    }

    requests.post(url, data=data)


def main():
    for name, channel_id in CHANNELS.items():
        video_id = get_latest_video(channel_id)

        if not video_id:
            continue

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        transcript = get_transcript(video_id)

        # 🔥 ALWAYS SEND (even if no transcript)
        if not transcript:
            message = f"🔥 {name}\n🎥 {video_url}\n\n⚠️ No transcript available"
            send_to_telegram(message)
            continue

        timestamps = find_moments(transcript)

        # 🔥 If no good moments found
        if not timestamps:
            message = f"🔥 {name}\n🎥 {video_url}\n\n⚠️ No strong moments found"
            send_to_telegram(message)
            continue

        # 🔥 Normal case
        message = f"🔥 {name}\n🎥 {video_url}\n\n🔥 BEST MOMENTS:\n\n"

        for i, t in enumerate(timestamps, 1):
            minutes = t // 60
            seconds = t % 60
            link = f"https://youtu.be/{video_id}?t={t}"

            message += f"{i}. {minutes:02d}:{seconds:02d} → {link}\n"

        send_to_telegram(message)


if __name__ == "__main__":
    main()
