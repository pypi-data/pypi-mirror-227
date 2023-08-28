#!/usr/bin/env python3

import argparse
import base64
import json
import logging
import os
import plistlib
import re
import shutil
import subprocess
import xmlrpc.client
from io import BytesIO
from multiprocessing import Pool, cpu_count
from pathlib import Path
from tkinter import Tk, Label

import numpy
from PIL import Image, ImageChops, ImageDraw, ImageTk
from pyzbar.pyzbar import decode
from rembg.bg import remove, new_session
from skimage.filters import threshold_otsu, gaussian
from skimage.measure import regionprops
from skimage.morphology import label, closing, square

IS_TESTING = os.environ.get("IS_TESTING", "").lower() in ["true", "1"]
LEAVE_IMAGES = os.environ.get("LEAVE_IMAGES", "").lower() in ["true", "1"]

# Defaults
SD_CARD_PATH = Path("/Volumes/EOS_DIGITAL")
if IS_TESTING:
    SD_CARD_PATH = Path.home() / "Pictures" / "Canon"
OUTPUT_PATH = Path.home() / "Desktop/eBay Pics"
ORIGINAL_OUTPUT_PATH = OUTPUT_PATH / "Original"
NB_TRIMMED_OUTPUT_PATH = OUTPUT_PATH / "NB_Trimmed"
NB_OUTPUT_PATH = OUTPUT_PATH / "NB"
TRIMMED_OUTPUT_PATH = OUTPUT_PATH / "Trimmed"

PHOTO_EXTENSIONS = ["JPG", "jpg", "CR2", "cr2", "PNG", "png", "JPEG", "jpeg"]
RGB = tuple[int, int, int]
logging.basicConfig(level=logging.INFO, filename="/tmp/ebay_pictures_tool.log")
logger = logging.getLogger(__name__)


def load_secrets_from_file() -> dict[str, str]:
    home = Path.home()
    secret_file_path = home / ".shiny" / "secret.json"

    try:
        with open(secret_file_path) as file:
            secret_file_json = json.load(file)
    except FileNotFoundError:
        logger.error(f"Secret file not found at {secret_file_path}.  Creating template file")
        root_project_path = Path(__file__).parent
        sample_secret_file_path = root_project_path / "secret.json.sample"
        os.makedirs(os.path.dirname(secret_file_path), exist_ok=True)
        shutil.copy(sample_secret_file_path, secret_file_path)

        return {}

    return secret_file_json


secrets = load_secrets_from_file()
ODOO_URL = secrets.get("odoo_url", "")
ODOO_DB = secrets.get("odoo_db", "")
ODOO_USERNAME = secrets.get("odoo_username", "")
ODOO_PASSWORD = secrets.get("odoo_password", "")


def get_brew_path() -> Path | None:
    try:
        architecture = subprocess.check_output(['uname', '-m']).decode('utf-8').strip()
    except Exception as e:
        logger.error(f"Failed to determine architecture: {e}")
        return None

    if architecture == "x86_64":
        return Path("/usr/local/bin")
    elif "arm" in architecture:
        return Path("/opt/homebrew/bin")
    else:
        logger.error(f"Unsupported architecture: {architecture}")
        raise ValueError(f"Unsupported architecture: {architecture}")


def restart_launch_agent(launch_agent_path: Path):
    try:
        uid = subprocess.check_output(["id", "-u"]).decode('utf-8').strip()
        domain = f"gui/{uid}"

        logger.info(f"Stopping launch agent at {launch_agent_path.stem}")

        # noinspection SpellCheckingInspection
        command_to_run = ["launchctl", "bootout", f"{domain}/{launch_agent_path.stem}"]
        subprocess.run(command_to_run)
        logger.info(" ".join(command_to_run))

        logger.info(f"Starting launch agent at {launch_agent_path.stem}")

        command_to_run = ["launchctl", "bootstrap", domain, launch_agent_path.as_posix()]
        subprocess.run(command_to_run)
        logger.info(" ".join(command_to_run))

        command_to_run = ["launchctl", "kickstart", "-k", f"{domain}/{launch_agent_path.stem}"]
        subprocess.run(command_to_run)
        logger.info(" ".join(command_to_run))

        logger.info("Loaded launch agent")
    except subprocess.CalledProcessError:
        logger.error("Failed to load launch agent")
        raise


def install_launch_agent():
    home = Path.home()
    launch_agent_dir = home / "Library" / "LaunchAgents"
    # noinspection SpellCheckingInspection
    launch_agent_name = "com.shiny.sdcardlistener.plist"
    launch_agent_path = launch_agent_dir / launch_agent_name

    root_project_dir = Path(__file__).parent
    plist_file_path = root_project_dir / launch_agent_name
    is_changed = False
    if not launch_agent_path.exists():
        is_changed = True
        logger.info(f"Installing launch agent at {launch_agent_path}")
        launch_agent_dir.mkdir(exist_ok=True)
        shutil.copy(plist_file_path, launch_agent_path)

    with open(launch_agent_path, "rb") as file:
        plist_data = plistlib.load(file)

    correct_script_path = get_brew_path() / "ebay_pictures_tool"
    if plist_data["ProgramArguments"][0] != correct_script_path.as_posix():
        is_changed = True
        logger.info(f"Updating launch agent path to {correct_script_path}")
        plist_data["ProgramArguments"][0] = correct_script_path.as_posix()

    correct_input_path = str(SD_CARD_PATH)
    if plist_data["QueueDirectories"][0] != correct_input_path:
        if "EnvironmentVariables" not in plist_data:
            plist_data["EnvironmentVariables"] = {}
        if IS_TESTING:
            plist_data["EnvironmentVariables"]["IS_TESTING"] = "True"
        else:
            plist_data["EnvironmentVariables"].pop("IS_TESTING", None)
        logger.info(f"Updating input path to {correct_input_path}")
        plist_data["QueueDirectories"][0] = correct_input_path
        is_changed = True

    if is_changed:
        with launch_agent_path.open("wb") as file:
            plistlib.dump(plist_data, file)
        restart_launch_agent(launch_agent_path)


def eject_sd_card(sd_card_path: Path) -> None:
    try:
        subprocess.run(["diskutil", "eject", sd_card_path])
        logger.info("Ejected SD card")
    except subprocess.CalledProcessError as error:
        logger.error(f"Failed to eject SD card: {error}")


def create_directories(
        paths_to_create: list[Path],
) -> bool:
    for output_path in paths_to_create:
        output_path.mkdir(exist_ok=True, parents=True)
    return True


def copy_images_from_sd_card(sd_card_path: Path, output_path: Path) -> list[Path]:
    files_to_process = []
    for ext in PHOTO_EXTENSIONS:
        for source_file in sd_card_path.rglob(f"*.{ext}"):
            destination_file = output_path / source_file.name
            shutil.copy(source_file, destination_file)
            logger.info(f"Processing {source_file.name}")
            files_to_process.append(destination_file)
            if not LEAVE_IMAGES:
                source_file.unlink()
    return files_to_process


def process_images(
        files_to_process: list[Path],
        nb_output_path: Path,
        trimmed_output_path: Path,
        nb_trimmed_output_path: Path,
        model_name,
        background_color,
) -> None:
    chunk_size = max(1, len(files_to_process) // (cpu_count() * 4))
    args = [
        (file_path, nb_output_path, trimmed_output_path, nb_trimmed_output_path, model_name, background_color)
        for file_path in files_to_process
    ]
    with Pool(cpu_count()) as pool:
        pool.starmap(process_image, args, chunksize=chunk_size)


def sanitize_filename(filename: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_-]', '', filename)


def decode_and_remove_qr_label(image: Image) -> (str | None, Image):
    image_np = numpy.array(image.convert('L'))
    decoded_objects = decode(image_np)

    for obj in decoded_objects:
        # Get the bounding rectangle
        x, y, w, h = obj.rect.left, obj.rect.top, obj.rect.width, obj.rect.height

        # Calculate the expanded rectangle dimensions
        expanded_w = x + w * 1.10
        expanded_h = y + h * 1.10

        adjusted_x = x - w * 0.10
        adjusted_y = y - h * 0.10

        coords = (
            (int(adjusted_x), int(adjusted_y)),
            (int(expanded_w), int(expanded_h))
        )

        image_draw = ImageDraw.Draw(image)
        image_draw.rectangle(coords, fill="white")
        sanitized_name = sanitize_filename(obj.data.decode('utf-8'))
        return sanitized_name, image

    return None, image


def generate_unique_filename(output_path: Path, filename: str) -> Path:
    base_name = output_path.joinpath(filename).stem
    extension = output_path.joinpath(filename).suffix

    counter = 1
    new_filepath = output_path / filename
    while new_filepath.exists():
        new_filepath = output_path / f"{base_name}_{counter}{extension}"
        counter += 1
    return new_filepath


def add_image_to_odoo(sku: str, image: Image) -> None:
    if sku and 0 < len(sku) < 10 and sku.isdigit():
        logger.info(f"Updating record {sku} with image")
        add_odoo_product_image(ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, sku, image)
    else:
        logger.warning(f"Record not found for SKU: {sku}")


def process_image(
        original_image_file_path: Path,
        nb_output_path: Path,
        trimmed_output_path: Path,
        nb_trimmed_output_path: Path,
        model_name: str,
        background_color: RGB,
) -> None:
    original_image = Image.open(original_image_file_path)

    # qr_data, original_image = decode_and_remove_qr_label(original_image)
    qr_data = None  # TODO: Remove this line when QR code is working
    output_file_name = original_image_file_path.stem
    if qr_data:
        output_file_name = qr_data
        logger.info(f"Found QR code with data: {qr_data}")
    else:
        logger.warning("No QR code found, using original filename.")

    logger.info(f"Removing background from {original_image_file_path.name}")

    cleaned_image_file_path = generate_unique_filename(nb_output_path, output_file_name + ".png")

    session = new_session(model_name)
    cleaned_image = remove(original_image, session=session)

    cleaned_image.save(cleaned_image_file_path)
    logger.info(f"Writing {cleaned_image_file_path.name}")

    trimmed_image = trim_image(cleaned_image)
    trimmed_image_file_path = generate_unique_filename(trimmed_output_path, output_file_name + ".png")
    logger.info(f"Trimmed {trimmed_image_file_path.name}")

    trimmed_image_with_bg = add_background_color(trimmed_image, background_color)
    trimmed_image_with_bg.save(trimmed_image_file_path, format="PNG")
    original_image.close()
    if ODOO_DB and qr_data:
        add_image_to_odoo(output_file_name, trimmed_image_with_bg)


def trim_image(image: Image) -> Image:
    background = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, background)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    cropped_image = diff.getbbox()
    if cropped_image:
        return image.crop(cropped_image)
    return image  # Return original image if no changes detected


def add_background_color(image: Image, color: RGB = (255, 255, 255)) -> Image:
    if image.mode in ("RGBA", "LA"):
        background = Image.new(image.mode[:-1], image.size, color)
        background.paste(image, image.split()[-1])
        return background
    else:
        return image


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process images from SD card")
    parser.add_argument(
        "-s",
        "--sd_card_path",
        type=str,
        default=str(SD_CARD_PATH),
        help="Path to SD card",
    )
    parser.add_argument(
        "-o",
        "--original_output_path",
        type=str,
        default=str(ORIGINAL_OUTPUT_PATH),
        help="Path to output directory",
    )
    parser.add_argument(
        "-nt",
        "--nb_trimmed_output_path",
        type=str,
        default=str(NB_TRIMMED_OUTPUT_PATH),
        help="Path to trimmed output directory",
    )
    parser.add_argument(
        "-n",
        "--nb_output_path",
        type=str,
        default=str(NB_OUTPUT_PATH),
        help="Path to no background output directory",
    )
    parser.add_argument(
        "-t",
        "--trimmed_output_path",
        type=str,
        default=str(TRIMMED_OUTPUT_PATH),
        help="Path to trimmed output directory",
    )
    parser.add_argument(
        "-b",
        "--background_color",
        type=parse_rgb,
        default=(255, 255, 255),
        help="Background color to add to trimmed images in (R,G,B) format",
    )
    # noinspection SpellCheckingInspection
    parser.add_argument(
        "-m",
        "--model_name",
        type=str,
        default="isnet-general-use",
        help="""Model name to use for background removal. Available options:
          - 'isnet-general-use': This model is optimal for cleanly cutting out the primary object, 
                                 but it will remove everything except the main subject.
          - 'u2net': This model doesn't cut as cleanly as 'isnet-general-use', 
                     but retains smaller parts in the pictures, such as screws or other minor details.
          - 'auto': This will automatically select the best model based on the number of objects in the image.
        Default is 'auto'.""",
    )

    return parser.parse_args()


def parse_rgb(color_string: str) -> RGB:
    try:
        r, g, b = map(int, color_string.strip("()").split(","))
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return r, g, b
        else:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid color format: {color_string}. Expected format: (R,G,B) with each value between 0 and 255."
        )


def add_odoo_product_image(url, db, username, password, product_sku, image: Image):
    # noinspection SpellCheckingInspection
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    # noinspection SpellCheckingInspection
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

    # 1. Find the product based on its SKU
    product_ids = models.execute_kw(
        db, uid, password,
        'product.import', 'search',
        [[['default_code', '=', product_sku]]]
    )

    if not product_ids:
        raise ValueError(f"No product found with SKU: {product_sku}")

    product_id = product_ids[0]  # Assuming there's only one unique SKU

    # 2. Read the image and encode it to base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # 3. Create a new image record linked to the product
    image_record_id = models.execute_kw(
        db, uid, password,
        'product.import.image', 'create',
        [{
            'image_data': image_data,
            'product_id': product_id
        }]
    )

    return image_record_id


def main() -> None:
    install_launch_agent()
    args = get_args()
    sd_card_path = Path(args.sd_card_path)
    original_output_path = Path(args.original_output_path)
    trimmed_output_path = Path(args.trimmed_output_path)
    nb_trimmed_output_path = Path(args.nb_trimmed_output_path)
    nb_output_path = Path(args.nb_output_path)
    if not sd_card_path.exists():
        logger.error(f"SD card not found at {sd_card_path}")
        return

    if create_directories(
            [original_output_path, trimmed_output_path, nb_output_path, nb_trimmed_output_path]
    ):
        copied_files = copy_images_from_sd_card(sd_card_path, original_output_path)
        eject_sd_card(sd_card_path)
        process_images(
            copied_files,
            nb_output_path,
            trimmed_output_path,
            nb_trimmed_output_path,
            args.model_name,
            args.background_color,
        )


if __name__ == "__main__":
    main()
