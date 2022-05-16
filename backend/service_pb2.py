"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\tfloorplan"$\n\x0eProcessRequest\x12\x12\n\nimage_data\x18\x01 \x01(\x0c" \n\x0fProcessResponse\x12\r\n\x05model\x18\x01 \x01(\x0c2K\n\x07Service\x12@\n\x07Process\x12\x19.floorplan.ProcessRequest\x1a\x1a.floorplan.ProcessResponseb\x06proto3')
_PROCESSREQUEST = DESCRIPTOR.message_types_by_name['ProcessRequest']
_PROCESSRESPONSE = DESCRIPTOR.message_types_by_name['ProcessResponse']
ProcessRequest = _reflection.GeneratedProtocolMessageType('ProcessRequest', (_message.Message,), {'DESCRIPTOR': _PROCESSREQUEST, '__module__': 'service_pb2'})
_sym_db.RegisterMessage(ProcessRequest)
ProcessResponse = _reflection.GeneratedProtocolMessageType('ProcessResponse', (_message.Message,), {'DESCRIPTOR': _PROCESSRESPONSE, '__module__': 'service_pb2'})
_sym_db.RegisterMessage(ProcessResponse)
_SERVICE = DESCRIPTOR.services_by_name['Service']
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _PROCESSREQUEST._serialized_start = 28
    _PROCESSREQUEST._serialized_end = 64
    _PROCESSRESPONSE._serialized_start = 66
    _PROCESSRESPONSE._serialized_end = 98
    _SERVICE._serialized_start = 100
    _SERVICE._serialized_end = 175