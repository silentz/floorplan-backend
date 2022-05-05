import grpc
from concurrent import futures

from .config import args
from .server import Server
from . import service_pb2_grpc as pb2_grpc


if __name__ == '__main__':
    thread_pool = futures.ThreadPoolExecutor(max_workers=args.app.workers)
    server = grpc.server(thread_pool)
    pb2_grpc.add_ServiceServicer_to_server(Server(), server)
    server.add_insecure_port(f'{args.app.host}:{args.app.port}')
    server.start()
    server.wait_for_termination()
