
## floorplan-backend

### Install

Run from project root:

```
helm install floorplan chart
```

### Inference

Use frontend or perform gRPC request on k8s service address using this schema:
```
syntax = "proto3";
package floorplan;

message ProcessRequest {
    bytes image_data = 1;
}


message ProcessResponse {
    bytes model = 1;
}


service Service {
    rpc Process (ProcessRequest) returns (ProcessResponse);
}
```
