import sys
import os
import json
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account

def initialize_youtube_client(credentials_file):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=scopes
    )
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

def upload_video(youtube, config):
    video_file = config["video_file"]

    request_body = {
        "snippet": {
            "title": config["title"],
            "description": config["description"],
            "tags": config["tags"],
            "categoryId": config["category_id"]
        },
        "status": {
            "privacyStatus": config["privacy"]
        }
    }

    media_chunk_size = 1024 * 1024 * 256  # 256MB
    insert_request = youtube.videos().insert(
        part=",".join(request_body.keys()),
        body=request_body,
        media_body=video_file,
        media_mime_type="video/mp4",
    )

    response = None
    try:
        response = insert_request.execute()
        print("Video uploaded successfully!")
        print("Video ID:", response["id"])
        return response
    except googleapiclient.errors.HttpError as e:
        print("An HTTP error occurred:", e)
    finally:
        if response is None:
            print("Video upload failed.")

def main(config_file_path):
    with open(config_file_path) as f:
        config = json.load(f)

        credentials_file = os.path.abspath(config["credentials_file"])

        youtube = initialize_youtube_client(credentials_file)
        upload_video(youtube, config)

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("No config file path was passed as argument.")
        sys.exit()
    
    config_file_path = args[1]
    main(config_file_path)
