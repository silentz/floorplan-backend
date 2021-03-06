import numpy as np
import tritonclient.http as tclient
from typing import Any, Dict, Tuple

from . import utils


class Service:

    def __init__(self, config: Dict[str, Any]):
        self._host = config.get('host', '127.0.0.1')
        self._port = config.get('port', 8000)
        self._model_name = config.get('model_name', 'floorplan')
        self._pad_value = config.get('pad_value', (255, 255, 255))
        self._image_size = config.get('image_size', 512)
        self._n_classes = config.get('n_classes', 11)

        client_url = f'{self._host}:{self._port}'
        self._client = tclient.InferenceServerClient(client_url)

    def _triton_request(self, input: np.ndarray) -> np.ndarray:
        batch_size = input.shape[0]
        inp_shape = [batch_size, 3,               self._image_size, self._image_size]
        out_shape = [batch_size, self._n_classes, self._image_size, self._image_size]

        inputs = [
                tclient.InferInput('input__0', inp_shape, "FP32"),
            ]

        outputs = [
                tclient.InferInput('output__0', out_shape, "FP32"),
            ]

        inputs[0].set_data_from_numpy(input, binary_data=True)
        model_out = self._client.infer(self._model_name, inputs, outputs=outputs)
        model_out = model_out.as_numpy('output__0')
        return model_out

    def _infer_model_multiple(self, image: np.ndarray) -> np.ndarray:
        inputs = [
                image,
                np.rot90(image, k=1, axes=(0, 1)),
                np.rot90(image, k=2, axes=(0, 1)),
                np.rot90(image, k=3, axes=(0, 1)),
                np.flipud(image),
                np.fliplr(image),
            ]

        batch = np.stack(inputs, axis=0)
        batch = np.transpose(batch, (0, 3, 1, 2))
        batch = batch.astype(np.float32)

        model_out = self._triton_request(batch)
        model_out = np.transpose(model_out, (0, 2, 3, 1))

        masks = [
                model_out[0],
                np.rot90(model_out[1], k=3, axes=(0, 1)),
                np.rot90(model_out[2], k=2, axes=(0, 1)),
                np.rot90(model_out[3], k=1, axes=(0, 1)),
                np.flipud(model_out[4]),
                np.fliplr(model_out[5]),
            ]

        mask = sum(masks)
        mask = np.argmax(mask, axis=2)
        mask = mask.astype(np.uint8)

        return mask

    def _infer_model_once(self, image: np.ndarray) -> np.ndarray:
        batch = np.expand_dims(image, axis=0)
        batch = np.transpose(batch, (0, 3, 1, 2))
        batch = batch.astype(np.float32)
        model_out = self._triton_request(batch)
        model_out = model_out[0]
        model_out = np.transpose(model_out, (1, 2, 0))
        mask = np.argmax(model_out, axis=2)
        return mask

    def infer(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        r_image = utils.resize_image(
                image=image,
                max_size=self._image_size,
            )

        p_image = utils.pad_image(
                image=r_image,
                pad_size=self._image_size,
                pad_value=self._pad_value,
            )

        p_mask = self._infer_model_once(p_image)

        r_mask = utils.unpad_image(
                image=p_mask,
                origin_height=r_image.shape[0],
                origin_width=r_image.shape[1],
            )

        return r_image, r_mask
