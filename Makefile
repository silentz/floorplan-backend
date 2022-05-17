SHELL := /bin/bash
.PHONY: protos triton run-triton push-triton backend push-backend envoy push-envoy frontend push-frontend


TRITON_IMAGE_NAME   := mepershin/floorplan-triton
BACKEND_IMAGE_NAME  := mepershin/floorplan-backend
ENVOY_IMAGE_NAME    := mepershin/floorplan-envoy
FRONTEND_IMAGE_NAME := mepershin/floorplan-frontend


protos:
	python -m grpc_tools.protoc \
		-I ./protos \
		--python_out=backend/backend/ \
		--grpc_python_out=backend/backend/ \
		--include_imports \
		--include_source_info \
		--descriptor_set_out=envoy/inference.pb \
		./protos/*.proto
	protol \
		--dont-create-package \
		--in-place \
		--python-out backend/backend/ \
		protoc \
			--proto-path=./protos \
			./protos/service.proto

triton:
	docker build triton/ -t ${TRITON_IMAGE_NAME}

run-triton:
	docker run -it -p8000:8000 -p8001:8001 --gpus=1 ${TRITON_IMAGE_NAME}

push-triton:
	docker push ${TRITON_IMAGE_NAME}:latest

backend:
	docker build backend/ -t ${BACKEND_IMAGE_NAME}

push-backend:
	docker push ${BACKEND_IMAGE_NAME}:latest

envoy:
	docker build envoy -t ${ENVOY_IMAGE_NAME}

push-envoy:
	docker push ${ENVOY_IMAGE_NAME}:latest

frontend:
	docker build frontend/ -t ${FRONTEND_IMAGE_NAME}

push-frontend:
	docker push ${FRONTEND_IMAGE_NAME}:latest
