import os

from PIL import Image

files = os.listdir("img/original_images")

for file in files:
    im = Image.open(f"img/original_images/{file}").convert("RGBA")

    pixels = im.load()

    for y in range(im.height):
        for x in range(im.width):
            pixel = pixels[x, y]
            if pixel[0] == 0 and pixel[1] >= 225 and pixel[2] == 0 and pixel[3] == 255:
                pixels[x, y] = (0, 0, 0, 255 - pixel[1])

    im.save(f"img/transparent_images/{file}", "PNG")
