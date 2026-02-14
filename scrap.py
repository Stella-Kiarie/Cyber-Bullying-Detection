import googleapiclient.discovery
import pandas as pd

def get_video_comments(video_id, api_key):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100  # You can loop this to get thousands
    )
    response = request.execute()

    comments = []
    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    
    return comments

# Example: Use a viral Kenyan video ID
api_key = "YOUR_API_KEY_HERE"
video_id = "kY3LRE7_2S0" 
data = get_video_comments(video_id, api_key)

# Save to CSV for your ML model
df = pd.DataFrame(data, columns=["comment_text"])
df.to_csv("sheng_bullying_data.csv", index=False)