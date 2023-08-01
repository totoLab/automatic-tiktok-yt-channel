import os
import subprocess
import requests
import json
import sys
import glob
import re

class Dirs:
    BUILD_DIR = os.path.abspath("build")
    BLUR_DIR = os.path.abspath("build/blur")
    DOWNLOAD_DIR = os.path.abspath("build/raw_videos")
    LOG_FILE_D = os.path.abspath("logs/ytdl.log")
    LOG_FILE_B = os.path.abspath("logs/ffmpeg_blur.log")
    LOG_FILE_C = os.path.abspath("logs/ffmpeg_concat.log")
    TITLES_FILE = os.path.abspath("service_files/titles.txt")


BUILD_DIR = Dirs.BUILD_DIR
BLUR_DIR = Dirs.BLUR_DIR
DOWNLOAD_DIR = Dirs.DOWNLOAD_DIR

def prepare_directories():
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    if not os.path.exists(BLUR_DIR):
        os.makedirs(BLUR_DIR)
    
    print("All necessary directories have been created.")

def get_data(url):
    headers = {"User-agent": "your bot 0.1"}
    response = requests.get(url, headers=headers)
    print(f"Got data from {url}")
    return response

def save_response(response, tmpFile):
    with open(tmpFile, "w") as file:
        file.write(response.text)

def parse_response_from_file(tmpFile):
    with open(tmpFile, "r") as file:
        data = json.load(file)

    urls = [item["data"]["url_overridden_by_dest"] for item in data["data"]["children"]
            if "url_overridden_by_dest" in item["data"]] [1:] #? first url is a discord invite

    print(f"Parsed data. Urls are:")
    for string in [f"{url}" for url in urls]:
        print(string)
    return urls

def download_videos(urls, output_dir=DOWNLOAD_DIR):
    with open(Dirs.LOG_FILE_D, "w") as log_file:
        for url in urls:
            command = ["yt-dlp", "--output", os.path.join(output_dir, "%(title)s.%(ext)s"), url]

            try:
                process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT)
                process.wait()
                print(f"Video downloaded: {url}")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while downloading {url}: {e}")
                sys.exit()

    print("All videos downloaded successfully.")

def blurring(file_list_path):
    with open(Dirs.TITLES_FILE, "w") as titles:
        for title in os.listdir(DOWNLOAD_DIR):
            titles.write(title)

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
    with open(Dirs.LOG_FILE_C, "w") as log_file:
        command = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_list_path,
            "-vcodec", "copy", "-acodec", "copy", final_output
        ]
        try:
            process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT)
            process.wait()
            print("Final video is ready.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during ffmpeg execution: {e}")
            sys.exit()


def clear_directory(directory):
    files = glob.glob(f"{directory}/*")
    for f in files:
        os.remove(f)

def clean_up(tmpFile):
    if os.path.exists(tmpFile):
        os.remove(tmpFile)
    clear_directory(BLUR_DIR)
    clear_directory(DOWNLOAD_DIR)
    
    print("Cleaned up unnecessary files.")
