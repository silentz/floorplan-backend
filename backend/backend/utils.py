import cv2
import numpy as np
from typing import Tuple, Union


def read_image(raw_image: bytes) -> Union[None, np.ndarray]:
    np_raw_image = np.fromstring(raw_image, np.uint8)
    image = cv2.imdecode(np_raw_image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def resize_image(image: np.ndarray,
                 max_size: int) -> np.ndarray:
    height, width, _ = image.shape
    new_width = max_size
    new_height = max_size

    if height >= width:
        new_width  = int((max_size / height) * width)
    else:
        new_height = int((max_size / width) * height)

    new_image = cv2.resize(
                    src=image,
                    dsize=(new_width, new_height),
                    interpolation=cv2.INTER_AREA)

    return new_image


def pad_image(image: np.ndarray,
              pad_size: int,
              pad_value: Tuple[int, int, int]) -> np.ndarray:
    pad_height = 0
    pad_width  = 0

    if image.shape[0] < pad_size:
        pad_height = pad_size - image.shape[0]

    if image.shape[1] < pad_size:
        pad_width = pad_size - image.shape[1]

    new_image = cv2.copyMakeBorder(
            src=image,
            top=0,
            bottom=pad_height,
            left=0,
            right=pad_width,
            borderType=cv2.BORDER_CONSTANT,
            value=pad_value)

    return new_image


def unpad_image(image: np.ndarray,
                origin_height: int,
                origin_width: int) -> np.ndarray:
    tx = image[:origin_height, :origin_width]
    return np.copy(tx)
