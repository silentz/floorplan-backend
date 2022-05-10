SHELL := /bin/bash
.PHONY: protos triton run-triton


TRITON_IMAGE_NAME := mepershin/floorplan-triton


protos:
	python -m grpc_tools.protoc \
		-I ./protos \
		--python_out=src/ \
		--grpc_python_out=src/ \
		./protos/*.proto
	protol \
		--dont-create-package \
		--in-place \
		--python-out src \
		protoc --proto-path=./protos \
		./protos/service.proto

triton:
	docker build triton/ -t ${TRITON_IMAGE_NAME}

run-triton:
	docker run -it -p8000:8000 -p8001:8001 ${TRITON_IMAGE_NAME}

push-triton:
	docker push ${TRITON_IMAGE_NAME}
