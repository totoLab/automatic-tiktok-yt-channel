import os
import subprocess
import requests
import json
import sys
import glob
import re

class Directories:
    BUILD_DIR = os.path.abspath("build")
    BLUR_DIR = os.path.abspath("build/blur")
    DOWNLOAD_DIR = os.path.abspath("build/raw_videos")

BUILD_DIR = Directories.BUILD_DIR
BLUR_DIR = Directories.BLUR_DIR
DOWNLOAD_DIR = Directories.DOWNLOAD_DIR

def prepare_directories():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    if not os.path.exists(BLUR_DIR):
        os.makedirs(BLUR_DIR)
    
    print("All necessary directories have been created.")

def get_data(url):
    headers = {"User-agent": "your bot 0.1"}
    response = requests.get(url, headers=headers)
    return response

def save_response(response, tmpFile):
    with open(tmpFile, "w") as file:
        file.write(response.text)

def parse_response_from_file(tmpFile):
    with open(tmpFile, "r") as file:
        data = json.load(file)

    urls = [item["data"]["url_overridden_by_dest"] for item in data["data"]["children"]
            if "url_overridden_by_dest" in item["data"]] [1:] #? first url is a discord invite

    print(f"Parsed data from {api_fetch_url}. Urls are:\n{[f"{url}\n" for url in urls]}")
    return urls

def download_videos(urls, output_dir=DOWNLOAD_DIR):
    for url in urls:
        command = ["yt-dlp", "--output", os.path.join(output_dir, "%(title)s.%(ext)s"), url]

        try:
            subprocess.run(command, check=True)
            print(f"Video downloaded: {url}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while downloading {url}: {e}")
            sys.exit()

    for filename in os.listdir(output_dir):
        if filename.endswith(".mp4"):
            new_filename = re.sub(r"`", " ", filename)  
            new_filename = re.sub(r"`", " ", new_filename)  
            os.rename(os.path.join(output_dir, filename), os.path.join(output_dir, new_filename))

    print("All videos downloaded and renamed successfully.")

def blurring(file_list_path):
    with open(file_list_path, "w") as file_list:
        for filename in os.listdir(DOWNLOAD_DIR):
            output_path = os.path.join(BLUR_DIR, filename)
            if filename.endswith(".mp4") and filename not in os.listdir(BLUR_DIR):
                input_path = os.path.join(DOWNLOAD_DIR, filename)
                subprocess.run([
                    "ffmpeg", "-y", "-i", input_path,
                    "-lavfi", "[0:v]scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16",
                    "-vb", "800K", output_path
                ])

            file_list.write(f"file `{os.path.abspath(output_path)}`\n")
    print("Applied necessary blurring.")


def join_to_final(file_list_path):
    final_output = os.path.join(BUILD_DIR, "final.mp4")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_list_path,
        "-vcodec", "copy", "-acodec", "copy", final_output
    ])
    print("Final video is ready.")

def clear_directory():
    files = glob.glob(f"{directory}/*")
    for f in files:
        os.remove(f)

def clean_up(tmpFile):
    os.remove(tmpFile)
    clear_directory(BLUR_DIR)
    clear_directory(DOWNLOAD_DIR)
    
    print("Cleaned up unnecessary files.")
