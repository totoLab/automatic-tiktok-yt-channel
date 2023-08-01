import sys, os
import make_video as m
import generate as gen
#import upload_video

def main(api_fetch_url, tmpFile, file_list_path, compilation_number, MANUAL=True, clean_up_toggle=False):
    if clean_up_toggle:
        m.clean_up(tmpFile)

    m.prepare_directories()

    response = m.get_data(api_fetch_url)
    m.save_response(response, tmpFile)
    urls = m.parse_response_from_file(tmpFile)

    m.download_videos(urls)

    m.blurring(file_list_path)
    
    m.join_to_final(file_list_path)

    #gen.title(m.Files.TITLES_FILE)
    title = f"{category} tiktok compilation #{compilation_number}"
    print(f"Title: {title}")

    if MANUAL:
        print("Now upload video to yt channel.")
    else:
        print("TODO: make the video upload automatically.")

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print(f"Not enough arguments, usage: {args[0]} [config path] [category of video]")
        sys.exit()
    config_path, category = args[1], args[2]
    limit, tmpFile, url, compilation_number = gen.update_compilation_db(config_path, category)
    api_fetch_url = f"{url}{limit}"
    file_list_path = os.path.join(m.Dirs.BUILD_DIR, "file_list.txt")
    main(api_fetch_url, tmpFile, file_list_path, compilation_number, clean_up_toggle=True)