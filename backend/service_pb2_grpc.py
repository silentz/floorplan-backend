
'Client and server classes corresponding to protobuf-defined services.'
import grpc
from . import service_pb2 as service__pb2

class ServiceStub(object):
    'Missing associated documentation comment in .proto file.'

    def __init__(self, channel):
        'Constructor.\n\n        Args:\n            channel: A grpc.Channel.\n        '
        self.Process = channel.unary_unary('/floorplan.Service/Process', request_serializer=service__pb2.ProcessRequest.SerializeToString, response_deserializer=service__pb2.ProcessResponse.FromString)

class ServiceServicer(object):
    'Missing associated documentation comment in .proto file.'

    def Process(self, request, context):
        'Missing associated documentation comment in .proto file.'
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_ServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {'Process': grpc.unary_unary_rpc_method_handler(servicer.Process, request_deserializer=service__pb2.ProcessRequest.FromString, response_serializer=service__pb2.ProcessResponse.SerializeToString)}
    generic_handler = grpc.method_handlers_generic_handler('floorplan.Service', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

class Service(object):
    'Missing associated documentation comment in .proto file.'

    @staticmethod
    def Process(request, target, options=(), channel_credentials=None, call_credentials=None, insecure=False, compression=None, wait_for_ready=None, timeout=None, metadata=None):
        return grpc.experimental.unary_unary(request, target, '/floorplan.Service/Process', service__pb2.ProcessRequest.SerializeToString, service__pb2.ProcessResponse.FromString, options, channel_credentials, insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
