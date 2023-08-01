import sys, os
import make_video as m
#import upload_video

def main(api_fetch_url, tmpFile, file_list_path, MANUAL=True, clean_up_toggle=False):
    m.prepare_directories()

    response = m.get_data(api_fetch_url)
    m.save_response(response, tmpFile)
    urls = m.parse_response_from_file(tmpFile)

    m.download_videos(urls)

    m.blurring(file_list_path)
    
    m.join_to_final(file_list_path)

    if clean_up_toggle:
        m.clean_up(tmpFile)

    if MANUAL:
        print("Now upload video to yt channel.")
    else:
        print("TODO: make the video upload automatically.")

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print(f"Not enough arguments, usage: {args[0]} [no. videos limit] [response dump file]")
        sys.exit()

    limit = 5
    tmpFile = "tmpFile.json"

    limit = int(args[1])
    tmpFile = os.path.abspath(args[2])
    file_list_path = os.path.join(m.Directories.BUILD_DIR, "file_list.txt")
    api_fetch_url = f"https://www.reddit.com/r/TikTokCringe/hot.json?limit={limit}"
    main(api_fetch_url, tmpFile, file_list_path)