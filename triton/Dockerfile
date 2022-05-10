FROM nvcr.io/nvidia/tritonserver:21.07-py3

COPY repo/ /repo

CMD ["/opt/tritonserver/bin/tritonserver", "--model-repository=/repo"]
