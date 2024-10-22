import json
import csv
import re

from googleapiclient.discovery import build
from config import API_KEY

youtube = build('youtube', 'v3', developerKey=API_KEY)

#makes the api call and fetches data categories
def fetch(video):
    request = youtube.videos().list(part="snippet,statistics,contentDetails,topicDetails", id=video)
    response = request.execute()

    if response:
        if response["items"]: #deals with privated or videos that no longer exist TwosetViolin RIP :(
            v = response["items"][0]

            data = {
                "title": v["snippet"]["title"],
                "description": v["snippet"]["description"],
                "channel_name": v["snippet"]["channelTitle"],
                "published_at": v["snippet"]["publishedAt"],
                "category_id": v["snippet"]["categoryId"],
                "view_count": v["statistics"].get("viewCount", "N/A"),
                "like_count": v["statistics"].get("likeCount", "N/A"),
                "comment_count": v["statistics"].get("commentCount", "N/A"),
                "duration": v["contentDetails"]["duration"]
            }

            return data
    return None

#uses category id and decodes into actual category
def fetch_category(category_id):
    request = youtube.videoCategories().list(part="snippet", id=category_id)
    response = request.execute()

    if response["items"]:
        category = response["items"][0]
        return category["snippet"]["title"]
    return "N/A"

def process(input_csv, output_csv):
    with open(input_csv, 'r', encoding='utf-8') as infile, open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=["Title", "Video URL", "Channel", "Category", "View Count", "Like Count", "Comment Count", "Duration"])
        writer.writeheader()

        for row in reader:
            url = row["Video URL"]
            match = re.search(r"v=([^&]+)", url)
            if match: #potentially if no url is included in the file
                video_id = match.group(1)

                if video_id:
                    video_details = fetch(video_id)

                    if video_details:
                        category_name = fetch_category(video_details["category_id"])

                        writer.writerow({
                            "Title": video_details["title"],
                            "Video URL": url,
                            "Channel": video_details["channel_name"],
                            "Category": category_name,
                            "View Count": video_details["view_count"],
                            "Like Count": video_details["like_count"],
                            "Comment Count": video_details["comment_count"],  
                            "Duration": video_details["duration"]
                        })

process('filtered_history.csv', 'videos6.csv')