import cv2
import numpy as np
from typing import Union


def read_image(raw_image: bytes) -> Union[None, np.ndarray]:
    np_raw_image = np.fromstring(raw_image, np.uint8)
    image = cv2.imdecode(np_raw_image, cv2.IMREAD_COLOR)
    return image
