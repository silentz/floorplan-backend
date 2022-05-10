import numpy as np
import tritonclient.grpc as tclient
from typing import Any, Dict

from . import utils


class Service:

    def __init__(self, config: Dict[str, Any]):
        self._host = config.get('host', '127.0.0.1')
        self._port = config.get('port', 8000)
        self._model_name = config.get('model_name', 'floorplan')
        self._pad_value = config.get('pad_value', (255, 255, 255))
        self._image_size = config.get('image_size', 512)

        client_url = f'{self._host}:{self._port}'
        self._client = tclient.InferenceServerClient(client_url)

    def _infer_model(self, image: np.ndarray) -> np.ndarray:
        #  inputs = [
        #          tclient.InferInput('input__0', [1, 3, self.MODEL_SIZE, self.MODEL_SIZE], "FP32"),
        #      ]

        #  outputs = [
        #          tclient.InferInput('output__0', [1, 10], "FP32"),
        #      ]

        #  inputs[0].set_data_from_numpy(image, binary_data=True)

        #  model_out = client.infer(model_name, inputs, outputs=outputs)
        #  model_out = model_out.as_numpy('output__0')[0]
        pass

    def infer(self, image: np.ndarray) -> np.ndarray:
        r_image = utils.resize_image(
                image=image,
                max_size=self._image_size,
            )

        p_image = utils.pad_image(
                image=r_image,
                pad_size=self._image_size,
                pad_value=self._pad_value,
            )

        print(p_image.shape)

