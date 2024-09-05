from logging import Logger
import logging
from bs4 import PageElement, Tag
import os
import sys
import base64
import mimetypes


def convert_image_to_base64(uri: str, logger: Logger | None = None) -> str | None:
    """Convert an image file to a base64 string."""
    if not logger:
        logger = logging.getLogger()

    # Extract the file path from the URI
    file_path = ""

    if sys.platform == "win32":
        file_path = uri.replace("file:///", "")
    else:
        file_path = uri.replace("file://", "")

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Determine the MIME type of the file
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
        logger.warning(f"The file {file_path} is not a valid image.")
        return None

    # Read the file content
    with open(file_path, "rb") as image_file:
        image_content = image_file.read()

    # Encode the content to base64
    base64_encoded = base64.b64encode(image_content).decode("utf-8")

    # Return the encoded string in the 'data:image/...' format
    return f"data:{mime_type};base64,{base64_encoded}"


def html_inline_images(soup, logger: Logger = None):
    """Converts all image tags with a 'src' attribute starting with 'file://' to inline base64 images."""
    if logger:
        logger.info("Converting inline images.")

    for img in soup.find_all("img"):
        if not img.has_attr("src"):
            continue
        if not isinstance(img, Tag):
            logger.warning(f"Invalid element, {img} is not a Tag.")
            continue

        if not img.has_attr("src"):
            logger.warning("The image tag does not have a 'src' attribute.")
            return None

        uri = img["src"]
        if not uri.startswith("file://"):
            logger.warning(f"The URI {uri} is not a file URI.")
            continue

        encoded_src = convert_image_to_base64(uri, logger)
        if encoded_src:
            img["src"] = encoded_src
            logger.info(f"  | {img['src']} -> (base64)")


def fix_image_alignment(soup: PageElement, logger: Logger = None):
    """(workaraound) convert <img align=*> to `float` style.
    and, move <img width=*>, <image height=*> to style attributes.
    """

    if logger:
        logger.info("Converting <img> alignment(workaround).")

    for img in soup.select("img"):
        try:
            if img.has_attr("class") and "twemoji" in img["class"]:
                continue

            styles = _parse_style(getattr(img, "style", ""))

            logger.debug(f"  | {img}")
            if img.has_attr("align"):
                if img["align"] == "left":
                    styles["float"] = "left"
                    styles["padding-right"] = "1rem"
                    styles["padding-bottom"] = "0.5rem"
                    img.attrs.pop("align")
                elif img["align"] == "right":
                    styles["float"] = "right"
                    styles["padding-left"] = "1rem"
                    styles["padding-bottom"] = "0.5rem"
                    img.attrs.pop("align")

            if img.has_attr("width"):
                styles["width"] = _convert_dimension(img["width"])
                img.attrs.pop("width")
            if img.has_attr("height"):
                styles["height"] = _convert_dimension(img["height"])
                img.attrs.pop("height")

            img["style"] = " ".join(f"{k}: {v};" for k, v in styles.items())
        except Exception as e:
            if logger:
                logger.warning(f"Failed to convert img align: {e}")
            pass


def images_size_to_half_in(section: Tag):
    def _split(s):
        for i, c in enumerate(s):
            if not c.isdigit():
                break
        number = s[:i]
        unit = s[i:].lstrip()
        return (number, unit)

    for img in section.find_all("img"):
        if not img.has_attr("style"):
            continue
        styles = _parse_style(img["style"])
        if not len(styles):
            continue

        for key in ["width", "height", "padding-left", "padding-right"]:
            if key in styles:
                (dim, u) = _split(styles[key])
                styles[key] = str(int(dim) / 2) + u
        img["style"] = " ".join(f"{k}: {v};" for k, v in styles.items())


def _parse_style(style_string: str) -> dict:
    styles = {}
    if style_string:
        for attr in style_string.split(";"):
            if not len(attr):
                continue
            val = attr.split(":", 2)
            styles[val[0].strip()] = val[1].strip()
    return styles


def _convert_dimension(dim_str: str) -> str:
    if dim_str.isdecimal():
        return dim_str + "px"
    return dim_str
