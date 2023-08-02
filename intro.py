import os
import subprocess
import json
import sys
from make_video import Dirs

from PIL import Image, ImageDraw, ImageFont

def generate_intro(category, compilation_number):
    input_image_path = os.path.join(Dirs.IMGS_DIR, f"{category}.png")
    output_image_path = os.path.join(Dirs.IMGS_DIR, f"out_{category}.png")
    text = f"#{compilation_number}"
    text_config = text, (1195, 600), 85, (255, 255, 255), 3, (0, 0, 0)

    add_text_to_image(input_image_path, output_image_path, text_config)


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
    generate_intro("funny", 2190)