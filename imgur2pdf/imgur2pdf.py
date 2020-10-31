import configparser
import os
import os.path
import shutil
from pathlib import Path

import click
import requests
from imgurpython import ImgurClient
from PIL import Image

SCREEN_SIZE = (1404, 1872)

APP_NAME = "imgur2pdf"
CONFIGURATION_FILE = ".imgur/config.ini"
CACHE_FOLDER = ".imgur/cache/"


def read_config():
    cfg = os.path.join(Path.home(), CONFIGURATION_FILE)
    parser = configparser.RawConfigParser()
    parser.read([cfg])
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv["%s.%s" % (section, key)] = value
    return rv


def download_file(url):
    filename = url.split("/")[-1]
    path = os.path.join(Path.home(), CACHE_FOLDER, filename)

    if not os.path.isfile(path):
        response = requests.get(url, stream=True)

        with open(path, "wb") as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    return path


def calculate_image_scaling(width, height):
    page_width, page_height = SCREEN_SIZE

    if width > height:
        aspect = page_width / float(width)
        return (page_width, height * aspect)
    else:
        aspect = page_height / float(height)
        return (width * aspect, page_height)


@click.command()
@click.version_option(version="0.1.1")
@click.argument("album_id")
def imgur2pdf(album_id):
    """
    Download an Imgur album to a PDF file.

    Find the ALBUM_ID in the URL: https://imgur.com/gallery/album_id
    """

    path = os.path.join(Path.home(), CACHE_FOLDER)
    os.makedirs(path, exist_ok=True)
    config = read_config()

    client_id = config[APP_NAME + ".client_id"]
    client_secret = config[APP_NAME + ".client_secret"]
    client = ImgurClient(client_id, client_secret)

    pages = []

    images_list = client.get_album_images(str(album_id))

    with click.progressbar(images_list, label="Downloading images") as bar:
        for item in bar:

            url = item.link
            filename = download_file(url)

            image = Image.open(filename)

            width, height = image.size
            if width > height:
                image = image.rotate(angle=90, expand=True, fillcolor="white")

            scaled_width, scaled_height = calculate_image_scaling(*image.size)
            image = image.resize((int(scaled_width), int(scaled_height)))

            pages.append(image.convert("RGB"))

    album_data = client.get_album(album_id)
    album_filename = album_data.title.replace(" ", "_") + ".pdf"

    first, rest = pages[0], pages[1:]

    first.save(
        album_filename, save_all=True, append_images=rest,
    )

    click.echo("PDF created: " + str(album_filename))
