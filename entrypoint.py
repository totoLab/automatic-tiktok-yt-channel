import make_video as m
import upload_video

def main(api_fetch_url, tmpFile, file_list_path, clean_up_toggle=False):
    m.prepare_directories()
    print("All necessary directories have been created.")

    response = m.get_data(api_fetch_url)
    m.save_response(response, tmpFile)
    urls = m.parse_response_from_file(tmpFile)
    print(f"Got and parsed data from {api_fetch_url}. Urls are:\n{urls}")

    m.download_videos(urls)
    m.blurring(file_list_path)
    print("Applied necessary blurring.")
    
    m.join_to_final(file_list_path)
    print("Final video is ready.")

    sys.exit()
    if clean_up_toggle:
        m.clean_up(tmpFile)
        print("Cleaned up unnecessary files.")

    print("Uploaded video to yt channel.")

if __name__ == "__main__":
    limit = 2
    tmpFile = "tmpFile.json"
    file_list_path = os.path.join(BUILD_DIR, "file_list.txt")
    api_fetch_url = f"https://www.reddit.com/r/TikTokCringe/hot.json?limit={limit}"
    main(api_fetch_url, tmpFile, file_list_path, clean_up_toggle=False)