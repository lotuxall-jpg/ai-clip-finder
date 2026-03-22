import requests
import xml.etree.ElementTree as ET
import re

# 🔹 TELEGRAM INFO
TELEGRAM_TOKEN = "8699414099:AAGA89Ig1Ijwn0gzWQM0jlfE1bYUi6L5970"
CHAT_ID = "8205944221"

# 🔹 CHANNEL ID (change later)
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"


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


# 🔥 Extract timestamps from transcript
def extract_timestamps(transcript):
    timestamps = []

    lines = transcript.split("\n")

    for line in lines:
        match = re.search(r"(\d+):(\d+)", line)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            total_seconds = minutes * 60 + seconds

            # Look for hype words
            if any(word in line.lower() for word in ["what", "no way", "bro", "oh my god"]):
                timestamps.append(total_seconds)

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
    video_id = get_latest_video(CHANNEL_ID)

    if not video_id:
        return

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    transcript = get_transcript(video_id)

    if not transcript:
        return

    timestamps = extract_timestamps(transcript)

    message = f"🎥 VIDEO:\n{video_url}\n\n🔥 BEST MOMENTS:\n\n"

    for i, t in enumerate(timestamps, 1):
        link = f"https://youtu.be/{video_id}?t={t}"
        minutes = t // 60
        seconds = t % 60

        message += f"{i}. {minutes:02d}:{seconds:02d} → {link}\n"

    send_to_telegram(message)


if __name__ == "__main__":
    main()
