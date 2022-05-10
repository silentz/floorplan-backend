FROM nvcr.io/nvidia/tritonserver:22.04-py3

COPY repo/ /repo

CMD ["/opt/tritonserver/bin/tritonserver", "--model-repository=/repo"]
