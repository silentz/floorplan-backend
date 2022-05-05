SHELL := /bin/bash
.PHONY: protos


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
