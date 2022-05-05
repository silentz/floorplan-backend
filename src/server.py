from . import service_pb2 as pb2
from . import service_pb2_grpc as pb2_grpc


class Server(pb2_grpc.ServiceServicer):

    def Process(self, request: pb2.ProcessRequest, context) -> pb2.ProcessResponse:
        print(type(context))
        return pb2.ProcessResponse()
