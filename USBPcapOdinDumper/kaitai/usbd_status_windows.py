# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class UsbdStatusWindows(KaitaiStruct):
    """
    .. seealso::
       Source - https://raw.githubusercontent.com/reactos/reactos/master/sdk/include/psdk/usb.h
    
    
    .. seealso::
       Source - https://docs.microsoft.com/en-us/previous-versions/windows/hardware/drivers/ff539136(v=vs.85)
    """

    class Code(Enum):
        crc = 1
        btstuff = 2
        data_toggle_mismatch = 3
        stall_pid = 4
        dev_not_responding = 5
        pid_check_failure = 6
        unexpected_pid = 7
        data_overrun = 8
        data_underrun = 9
        reserved1 = 10
        reserved2 = 11
        buffer_overrun = 12
        buffer_underrun = 13
        not_accessed = 15
        fifo = 16
        xact_error = 17
        babble_detected = 18
        data_buffer_error = 19
        endpoint_halted = 48
        invalid_urb_function = 512
        invalid_parameter = 768
        error_busy = 1024
        invalid_pipe_handle = 1536
        no_bandwidth = 1792
        internal_hc_error = 2048
        error_short_transfer = 2304
        bad_start_frame = 2560
        isoch_request_failed = 2816
        frame_control_owned = 3072
        frame_control_not_owned = 3328
        not_supported = 3584
        invalid_configuration_descriptor = 3840
        insufficient_resources = 4096
        set_config_failed = 8192
        buffer_too_small = 12288
        interface_not_found = 16384
        invalid_pipe_flags = 20480
        timeout = 24576
        device_gone = 28672
        status_not_mapped = 32768
        hub_internal_error = 36864
        canceled = 65536
        iso_not_accessed_by_hw = 131072
        iso_td_error = 196608
        iso_na_late_usbport = 262144
        iso_not_accessed_late = 327680
        bad_descriptor = 1048576
        bad_descriptor_blen = 1048577
        bad_descriptor_type = 1048578
        bad_interface_descriptor = 1048579
        bad_endpoint_descriptor = 1048580
        bad_interface_assoc_descriptor = 1048581
        bad_config_desc_length = 1048582
        bad_number_of_interfaces = 1048583
        bad_number_of_endpoints = 1048584
        bad_endpoint_address = 1048585
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.error = self._io.read_bits_int_le(1) != 0
        self.pending = self._io.read_bits_int_le(1) != 0
        self.reserved = self._io.read_bits_int_le(2)
        self.code = KaitaiStream.resolve_enum(UsbdStatusWindows.Code, self._io.read_bits_int_le(28))


