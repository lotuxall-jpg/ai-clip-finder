import requests
import xml.etree.ElementTree as ET

CHANNEL_ID = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # TEMP test channel (Google Devs)

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


def main():
    video_id = get_latest_video(CHANNEL_ID)

    if not video_id:
        print("❌ No video found")
        return

    print(f"🎥 Video ID: {video_id}")

    transcript = get_transcript(video_id)

    if not transcript:
        print("❌ No transcript found")
        return

    moments = find_viral_moments(transcript)

    print("\n🔥 Viral Moments:\n")
    for i, moment in enumerate(moments, 1):
        print(f"{i}. {moment}\n")


if __name__ == "__main__":
    main()
