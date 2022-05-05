SHELL := /bin/bash
.PHONY: protos


protos:
	docker run -v ${PWD}/protos/:/defs namely/protoc-all -f service.proto -l python
	mv ./protos/gen/pb_python/service_pb2.py src/
	mv ./protos/gen/pb_python/service_pb2_grpc.py src/
	rm -rf ./protos/gen/
