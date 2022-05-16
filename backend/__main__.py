import grpc
from concurrent import futures

from . import config
from . import model
from . import server
from . import service_pb2_grpc as pb2_grpc


if __name__ == '__main__':
    thread_pool = futures.ThreadPoolExecutor(max_workers=config.args.app.workers)
    grpc_server = grpc.server(thread_pool)

    model_srv = model.Service(config.args.triton)
    service = server.Server(config.args.input, model_srv)

    pb2_grpc.add_ServiceServicer_to_server(service, grpc_server)
    grpc_server.add_insecure_port(f'{config.args.app.host}:{config.args.app.port}')
    grpc_server.start()
    grpc_server.wait_for_termination()
