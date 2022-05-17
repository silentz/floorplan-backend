
'Generated protocol buffer code.'
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from .google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='service.proto', package='floorplan', syntax='proto3', serialized_options=None, create_key=_descriptor._internal_create_key, serialized_pb=b'\n\rservice.proto\x12\tfloorplan\x1a\x1cgoogle/api/annotations.proto"$\n\x0eProcessRequest\x12\x12\n\nimage_data\x18\x01 \x01(\x0c" \n\x0fProcessResponse\x12\r\n\x05model\x18\x01 \x01(\x0c2]\n\x07Service\x12R\n\x07Process\x12\x19.floorplan.ProcessRequest\x1a\x1a.floorplan.ProcessResponse"\x10\x82\xd3\xe4\x93\x02\n"\x08/processb\x06proto3', dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR])
_PROCESSREQUEST = _descriptor.Descriptor(name='ProcessRequest', full_name='floorplan.ProcessRequest', filename=None, file=DESCRIPTOR, containing_type=None, create_key=_descriptor._internal_create_key, fields=[_descriptor.FieldDescriptor(name='image_data', full_name='floorplan.ProcessRequest.image_data', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=b'', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=58, serialized_end=94)
_PROCESSRESPONSE = _descriptor.Descriptor(name='ProcessResponse', full_name='floorplan.ProcessResponse', filename=None, file=DESCRIPTOR, containing_type=None, create_key=_descriptor._internal_create_key, fields=[_descriptor.FieldDescriptor(name='model', full_name='floorplan.ProcessResponse.model', index=0, number=1, type=12, cpp_type=9, label=1, has_default_value=False, default_value=b'', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR, create_key=_descriptor._internal_create_key)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=96, serialized_end=128)
DESCRIPTOR.message_types_by_name['ProcessRequest'] = _PROCESSREQUEST
DESCRIPTOR.message_types_by_name['ProcessResponse'] = _PROCESSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
ProcessRequest = _reflection.GeneratedProtocolMessageType('ProcessRequest', (_message.Message,), {'DESCRIPTOR': _PROCESSREQUEST, '__module__': 'service_pb2'})
_sym_db.RegisterMessage(ProcessRequest)
ProcessResponse = _reflection.GeneratedProtocolMessageType('ProcessResponse', (_message.Message,), {'DESCRIPTOR': _PROCESSRESPONSE, '__module__': 'service_pb2'})
_sym_db.RegisterMessage(ProcessResponse)
_SERVICE = _descriptor.ServiceDescriptor(name='Service', full_name='floorplan.Service', file=DESCRIPTOR, index=0, serialized_options=None, create_key=_descriptor._internal_create_key, serialized_start=130, serialized_end=223, methods=[_descriptor.MethodDescriptor(name='Process', full_name='floorplan.Service.Process', index=0, containing_service=None, input_type=_PROCESSREQUEST, output_type=_PROCESSRESPONSE, serialized_options=b'\x82\xd3\xe4\x93\x02\n"\x08/process', create_key=_descriptor._internal_create_key)])
_sym_db.RegisterServiceDescriptor(_SERVICE)
DESCRIPTOR.services_by_name['Service'] = _SERVICE
