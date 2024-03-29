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
    INTRO_TEMP = os.path.abspath("build/intro_templates")
    INTRO_DIR = os.path.abspath("build/intro")
    LOG_DIR = os.path.abspath("logs")
    SERVICE_DIR = os.path.abspath("service_files")
    
class Files:
    LOG_FILE_D = os.path.join(Dirs.LOG_DIR, "ytdl.log")
    LOG_FILE_B = os.path.join(Dirs.LOG_DIR, "ffmpeg_blur.log")
    LOG_FILE_C = os.path.join(Dirs.LOG_DIR, "ffmpeg_concat.log")
    LOG_FILE_I = os.path.join(Dirs.LOG_DIR, "ffmpeg_intro.log")
    TITLES_FILE = os.path.join(Dirs.SERVICE_DIR, "titles.txt")

def prepare_directories():
    for dir_attr in dir(Dirs):
        if dir_attr.startswith('__') or not isinstance(getattr(Dirs, dir_attr), str):
            continue  # Skip special attributes and non-string attributes

        directory_path = getattr(Dirs, dir_attr)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    
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


def download_videos(urls, output_dir=Dirs.DOWNLOAD_DIR):
    with open(Files.LOG_FILE_D, "w") as log_file:
        for url in urls:
            download_command = ["yt-dlp", "--output", os.path.join(output_dir, "%(title)s.%(ext)s"), url]

            try:
                # Download the video using yt-dlp
                process = subprocess.Popen(download_command, stdout=log_file, stderr=subprocess.STDOUT)
                process.wait()
                print(f"Video downloaded: {url}")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while downloading {url}: {e}")
                sys.exit()

            # Get the downloaded video file path
            video_file = os.path.join(output_dir, os.path.basename(url) + ".mp4")

            # Reencode the video with the most compatible formats using ffmpeg
            reencode_command = ["ffmpeg", "-i", video_file, "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", "-y", video_file]

            try:
                process = subprocess.Popen(reencode_command, stdout=log_file, stderr=subprocess.STDOUT)
                process.wait()
                print(f"Video reencoded: {url}")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while reencoding {url}: {e}")
                sys.exit()

    print("All videos downloaded and reencoded successfully.")

def blurring(file_list_path):
    with open(Files.TITLES_FILE, "w") as titles:
        for title in os.listdir(Dirs.DOWNLOAD_DIR):
            titles.write(title)

    with open(file_list_path, "a") as file_list:
        with open(Files.LOG_FILE_B, "w") as log_file:
            for i, filename in enumerate( os.listdir(Dirs.DOWNLOAD_DIR) ):
                output_path = os.path.join(Dirs.BLUR_DIR, filename)
                if filename.endswith(".mp4") and filename not in os.listdir(Dirs.BLUR_DIR):
                    input_path = os.path.join(Dirs.DOWNLOAD_DIR, filename)
                    command = [
                        "ffmpeg", "-y", "-i", input_path,
                        "-lavfi", "[0:v]fps=30,scale=ih*16/9:-1,boxblur=luma_radius=min(h\,w)/20:luma_power=1:chroma_radius=min(cw\,ch)/20:chroma_power=1[bg];[bg][0:v]overlay=(W-w)/2:(H-h)/2,crop=h=iw*9/16",
                        "-c:v", "libx264",  # Video codec
                        "-c:a", "aac",      # Audio codec
                        "-strict", "experimental", "-b:a", "192k",  # Audio settings (you can adjust the bitrate if needed)
                        "-vb", "800K", output_path,
                    ]
                    try:
                        process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT)
                        process.wait()
                        print(f"Video blurred: {filename[:30]}...", end=" -> ")
                    except subprocess.CalledProcessError as e:
                        print(f"Error occurred while blurring {filename}: {e}")
                        sys.exit()

                    new_filename = f"{i}.mp4" 
                    new_path = os.path.join(Dirs.BLUR_DIR, new_filename)
                    os.rename(output_path, new_path)
                    print(f"Renamed to {new_filename}")
                    file_list.write(f"file {os.path.abspath(new_path)}\n")

    print("Applied necessary blurring, renamed files and created list of files to concat.")


def join_to_final(file_list_path):
    final_output = os.path.join(Dirs.BUILD_DIR, "final.mp4")
    with open(Files.LOG_FILE_C, "w") as log_file:
        command = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_list_path,
            "-c:v", "copy",  # Copy the video codec as before
            "-c:a", "copy",  # Use same audio codec
            "-strict", "experimental", "-b:a", "192k",
            final_output
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
    clear_directory(Dirs.BLUR_DIR)
    clear_directory(Dirs.DOWNLOAD_DIR)
    clear_directory(Dirs.INTRO_DIR)
    
    print("Cleaned up unnecessary files.")
