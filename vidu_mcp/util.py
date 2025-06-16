import os
import base64
from vidu_mcp.exceptions import ViduRequestError


def del_input_images(
        images: list[str],
) -> list[str]:
    input_images = []
    for image in images:
        image = del_input_image(image)
        input_images.append(image)

    return input_images


def del_input_image(
        image: str
) -> str:
    if not isinstance(image, str):
        raise ViduRequestError(f"image must be a string, got {type(image)}")
    if not image.startswith(("http://", "https://", "data:")):
        # if local image, convert to dataurl
        if not os.path.exists(image):
            raise ViduRequestError(f"image does not exist: {image}")
        with open(image, "rb") as f:
            image_data = f.read()
            image = f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"

    return image
