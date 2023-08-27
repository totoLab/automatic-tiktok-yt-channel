import sys, os
import intro
import make_video as m
import config as cfg
#import upload_video

NUMBER_OF_STEPS = 8

def is_enabled(sequence, index):
    if index >= len(sequence):
        print("Error: index too large.")
        sys.exit()
    return sequence[index] == "1"

def main(config, api_fetch_url, tmpFile, file_list_path, compilation_number, exec_sequence="1"*NUMBER_OF_STEPS):

    if is_enabled(exec_sequence, 0):
        m.clean_up(tmpFile)

    if is_enabled(exec_sequence, 1):
        m.prepare_directories()

    if is_enabled(exec_sequence, 2):
        response = m.get_data(api_fetch_url)
        m.save_response(response, tmpFile)
        urls = m.parse_response_from_file(tmpFile)

    if is_enabled(exec_sequence, 3):
        intro.generate_intro(file_list_path, config["font_path"], category, compilation_number)

    if is_enabled(exec_sequence, 4):
        m.download_videos(urls)

    if is_enabled(exec_sequence, 5):
        m.blurring(file_list_path)

    if is_enabled(exec_sequence, 6):
        m.join_to_final(file_list_path)

    if is_enabled(exec_sequence, 7):
        title = f"{category} tiktok compilation #{compilation_number}"
        print(f"Title: {title}")

        print("Now upload video to yt channel.")
    else:
        print("TODO: make the video upload automatically.")

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print(f"Not enough arguments, usage: {args[0]} [config path] [category of video]")
        sys.exit()
    config_path, category = args[1], args[2]
    config, limit, tmpFile, url, compilation_number = cfg.update_compilation_db(config_path, category)
    api_fetch_url = f"{url}{limit}"
    file_list_path = os.path.join(m.Dirs.BUILD_DIR, "file_list.txt")

    if len(args) >= 3:
        exec_sequence = args[3]
        assert(len(exec_sequence) == NUMBER_OF_STEPS)
        assert(all(char in ["0", "1"] for char in exec_sequence))

    main(config, api_fetch_url, tmpFile, file_list_path, compilation_number, exec_sequence)
