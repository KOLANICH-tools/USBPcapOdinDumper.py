# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class WindowsUrb(KaitaiStruct):

    class UrbFunction(Enum):
        select_configuration = 0
        select_interface = 1
        abort_pipe = 2
        take_frame_length_control = 3
        release_frame_length_control = 4
        get_frame_length = 5
        set_frame_length = 6
        get_current_frame_number = 7
        control_transfer = 8
        bulk_or_interrupt_transfer = 9
        isoch_transfer = 10
        get_descriptor_from_device = 11
        set_descriptor_to_device = 12
        set_feature_to_device = 13
        set_feature_to_interface = 14
        set_feature_to_endpoint = 15
        clear_feature_to_device = 16
        clear_feature_to_interface = 17
        clear_feature_to_endpoint = 18
        get_status_from_device = 19
        get_status_from_interface = 20
        get_status_from_endpoint = 21
        reserved_0x0016 = 22
        vendor_device = 23
        vendor_interface = 24
        vendor_endpoint = 25
        class_device = 26
        class_interface = 27
        class_endpoint = 28
        reserve_0x001d = 29
        sync_reset_pipe = 30
        class_other = 31
        vendor_other = 32
        get_status_from_other = 33
        clear_feature_to_other = 34
        set_feature_to_other = 35
        get_descriptor_from_endpoint = 36
        set_descriptor_to_endpoint = 37
        get_configuration = 38
        get_interface = 39
        get_descriptor_from_interface = 40
        set_descriptor_to_interface = 41
        get_ms_feature_descriptor = 42
        reserved_0x002b = 43
        reserved_0x002c = 44
        reserved_0x002d = 45
        reserved_0x002e = 46
        reserved_0x002f = 47
        sync_reset_pipe = 48
        sync_clear_stall = 49
        control_transfer_ex = 50
        reserved_0x0033 = 51
        reserved_0x0034 = 52
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        pass


