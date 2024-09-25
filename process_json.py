import json
import csv

# For processing json watch history into a dataset

JSON_FILE = "watch-history.json" 
CSV_FILE = "watch-history.csv"

# load in file
with open(JSON_FILE, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extract columns data
with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as csv_file:
    # open output file
    fout = csv.writer(csv_file)
    fout.writerow(['Title', 'Video URL', 'Channel', 'Date Watched', 'Ad?'])
    
    # process each entry
    for item in data:
        title = item.get('title', 'No Title')
        video_url = item.get('titleUrl', 'No URL')
        date = item.get('time', 'No Date')
        ad_status = False
        
        # Try to get channel, json includes youtube ads so those either 
        # have a channel or are N/A
        if 'subtitles' in item:
            channel_name = item['subtitles'][0].get('name', 'N/A')
        else:
            channel_name = 'N/A'  

        # further checks for ad status
        if 'details' in item:
            ad_status = True

        # write data row
        fout.writerow([title, video_url, channel_name, date, ad_status])