import requests
import xml.etree.ElementTree as ET

# 🔹 ADD YOUR TELEGRAM INFO HERE
TELEGRAM_TOKEN = "8699414099:AAGA89Ig1Ijwn0gzWQM0jlfE1bYUi6L5970"
CHAT_ID = "8205944221"

# 🔹 CHANNEL ID (change later to Kai Cenat etc.)
CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"


def get_latest_video(channel_id):
    try:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        response = requests.get(url)

        root = ET.fromstring(response.content)

        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            video_id = entry.find("{http://www.youtube.com/xml/schemas/2015}videoId").text
            return video_id

    except Exception as e:
        print("❌ Error getting video:", e)
        return None


def get_transcript(video_id):
    try:
        url = f"https://youtubetranscript.com/?server_vid2={video_id}"
        response = requests.get(url)
        return response.text

    except Exception as e:
        print("❌ Transcript error:", e)
        return ""


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


def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        data = {
            "chat_id": CHAT_ID,
            "text": message
        }

        requests.post(url, data=data)

    except Exception as e:
        print("❌ Telegram error:", e)


def main():
    video_id = get_latest_video(CHANNEL_ID)

    if not video_id:
        print("❌ No video found")
        return

    transcript = get_transcript(video_id)

    if not transcript:
        print("❌ No transcript found")
        return

    moments = find_viral_moments(transcript)

    message = f"🎥 Video ID: {video_id}\n\n🔥 Viral Moments:\n\n"

    for i, moment in enumerate(moments, 1):
        message += f"{i}. {moment}\n\n"

    send_to_telegram(message)


if __name__ == "__main__":
    main()
