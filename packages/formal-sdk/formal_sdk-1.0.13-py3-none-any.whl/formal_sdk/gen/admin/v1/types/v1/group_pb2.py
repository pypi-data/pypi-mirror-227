# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: admin/v1/types/v1/group.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x61\x64min/v1/types/v1/group.proto\x12\x11\x61\x64min.v1.types.v1\x1a\x1fgoogle/protobuf/timestamp.proto\"\xaa\x02\n\x05Group\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12\x16\n\x06\x61\x63tive\x18\x04 \x01(\x08R\x06\x61\x63tive\x12\x16\n\x06status\x18\x05 \x01(\tR\x06status\x12/\n\x05roles\x18\x06 \x03(\x0b\x32\x19.admin.v1.types.v1.DbUserR\x05roles\x12\x39\n\ncreated_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\tcreatedAt\x12\x19\n\x08user_ids\x18\x08 \x03(\tR\x07userIds\x12$\n\x0e\x64sync_group_id\x18\t \x01(\tR\x0c\x64syncGroupId\"\xfc\x01\n\x06\x44\x62User\x12\x0e\n\x02id\x18\x01 \x01(\tR\x02id\x12\x1f\n\x0b\x64\x62_username\x18\x02 \x01(\tR\ndbUsername\x12\x16\n\x06\x61\x63tive\x18\x03 \x01(\x08R\x06\x61\x63tive\x12\x16\n\x06status\x18\x04 \x01(\tR\x06status\x12\x12\n\x04type\x18\x05 \x01(\tR\x04type\x12\x1b\n\texpire_at\x18\x06 \x01(\x03R\x08\x65xpireAt\x12\x1d\n\ncreated_at\x18\x07 \x01(\x03R\tcreatedAt\x12\x1d\n\nupdated_at\x18\x08 \x01(\x03R\tupdatedAt\x12\"\n\rdsync_user_id\x18\t \x01(\tR\x0b\x64syncUserIdB\xdd\x01\n\x15\x63om.admin.v1.types.v1B\nGroupProtoP\x01ZQgithub.com/formalco/control-plane/backend/admin-api/gen/admin/v1/types/v1;typesv1\xa2\x02\x03\x41VT\xaa\x02\x11\x41\x64min.V1.Types.V1\xca\x02\x11\x41\x64min\\V1\\Types\\V1\xe2\x02\x1d\x41\x64min\\V1\\Types\\V1\\GPBMetadata\xea\x02\x14\x41\x64min::V1::Types::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'admin.v1.types.v1.group_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\025com.admin.v1.types.v1B\nGroupProtoP\001ZQgithub.com/formalco/control-plane/backend/admin-api/gen/admin/v1/types/v1;typesv1\242\002\003AVT\252\002\021Admin.V1.Types.V1\312\002\021Admin\\V1\\Types\\V1\342\002\035Admin\\V1\\Types\\V1\\GPBMetadata\352\002\024Admin::V1::Types::V1'
  _globals['_GROUP']._serialized_start=86
  _globals['_GROUP']._serialized_end=384
  _globals['_DBUSER']._serialized_start=387
  _globals['_DBUSER']._serialized_end=639
# @@protoc_insertion_point(module_scope)
