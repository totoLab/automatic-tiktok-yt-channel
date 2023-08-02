import os
import subprocess
import json
import sys
from make_video import Dirs, Files

from PIL import Image, ImageDraw, ImageFont

def generate_intro(file_list_path, category, compilation_number):
    image_path = generate_thumbnail(category, compilation_number)
    music_path = os.path.join(Dirs.INTRO_TEMP, "intro_music.mp3")
    final_output = os.path.join(Dirs.INTRO_DIR, "intro_video.mp4")

    with open(Files.LOG_FILE_I, "w") as log_file:
        command = [
            "ffmpeg", "-y", "-i", music_path, "-loop", "1", "-i", image_path,
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
            "-c:a", "aac", "-shortest", final_output
        ]
        try:    
            process = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT)
            process.wait()
            print("Intro is ready.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred during ffmpeg execution: {e}")
            sys.exit()

    with open(file_list_path, "w") as file_list:
        file_list.write(f"file {final_output}\n")

def generate_thumbnail(category, compilation_number):
    input_image_path = os.path.join(Dirs.INTRO_TEMP, f"{category}.png")
    output_image_path = os.path.join(Dirs.INTRO_DIR, f"{category}.png")
    text = f"#{compilation_number}"
    text_config = text, (1195, 600), 85, (255, 255, 255), 3, (0, 0, 0)

    add_text_to_image(input_image_path, output_image_path, text_config)
    return output_image_path


def add_text_to_image(input_image_path, output_image_path, text_config):
    text, position, font_size, font_color, border_width, border_color = text_config

    # Open the image
    image = Image.open(input_image_path)

    # Load the "opensans.ttf" font (replace 'opensans.ttf' with the path to the "opensans.ttf" font file)
    font = ImageFont.truetype('opensans.ttf', font_size)
    border_font = ImageFont.truetype('opensans.ttf', font_size + border_width)
    # Create a new ImageDraw object with the image as a parameter
    draw = ImageDraw.Draw(image)

    # Draw the text outline
    draw.text(position, text, font=border_font, fill=border_color, anchor="rs", align="right")

    draw.text(position, text, font=font, fill=font_color, anchor="rs", align="right")
    
    # Save the image with the added text
    image.save(output_image_path)

if __name__ == "__main__":
    generate_intro(os.path.join(Dirs.BUILD_DIR, "file_list.txt"), "funny", 2190)