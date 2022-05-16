import grpc
import numpy as np
from typing import Any, Dict

from . import model
from . import render
from . import utils
from . import service_pb2 as pb2
from . import service_pb2_grpc as pb2_grpc


class Server(pb2_grpc.ServiceServicer):


    def __init__(self, config: Dict[str, Any],
                       model_srv: model.Service,
                       render_srv: render.Service):
        super().__init__()
        self._model_srv = model_srv
        self._render_srv = render_srv
        self._min_image_width  = config.get('min_image_width', 32)
        self._min_image_height = config.get('min_image_height', 32)


    def Process(self, request: pb2.ProcessRequest,
                      context: grpc.ServicerContext) -> pb2.ProcessResponse:

        image = utils.read_image(request.image_data)

        if image is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('broken input image')
            return pb2.ProcessResponse()

        if not isinstance(image, np.ndarray):
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('invalid image internal data type')
            return pb2.ProcessResponse()

        if len(image.shape) != 3:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('image is expected to have 3 color channels')
            return pb2.ProcessResponse()

        if image.shape[0] < self._min_image_height:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'image height is expected to be {self._min_image_height} or more')
            return pb2.ProcessResponse()

        if image.shape[1] < self._min_image_width:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f'image width is expected to be {self._min_image_width} or more')
            return pb2.ProcessResponse()

        image, mask = self._model_srv.infer(image)

        np.save('mask.npy', mask, allow_pickle=False)

        model_bytes = self._render_srv.render(image, mask)

        return pb2.ProcessResponse(model=model_bytes)
