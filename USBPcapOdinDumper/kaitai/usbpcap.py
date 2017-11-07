# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

from . import usbd_status_windows
from . import usb_pcap_endpoint_number
class Usbpcap(KaitaiStruct):
    """A native pcap header of [usbpcap](https://github.com/desowin/usbpcap) - an app to capture USB frames in Windows OSes.
    
    .. seealso::
       Source - https://desowin.org/usbpcap/captureformat.html
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Usbpcap.Header(self._io, self, self._root)
        self.data = self._io.read_bytes(self.data_size)

    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header_size = self._io.read_u2le()
            self._raw_header_main = self._io.read_bytes((self.header_size - 2))
            _io__raw_header_main = KaitaiStream(BytesIO(self._raw_header_main))
            self.header_main = Usbpcap.Header.HeaderMain(_io__raw_header_main, self, self._root)

        class HeaderMain(KaitaiStruct):

            class TransferType(Enum):
                isochronous = 0
                interrupt = 1
                control = 2
                bulk = 3
                irp_info = 254
                unknown = 255
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.io_request_packet_id = self._io.read_u8le()
                self.usbd_status_windows_code = usbd_status_windows.UsbdStatusWindows(self._io)
                self.urb_function = self._io.read_u2le()
                self.io_request_info = Usbpcap.Header.HeaderMain.Info(self._io, self, self._root)
                self.bus = self._io.read_u2le()
                self.device_address = self._io.read_u2le()
                self.endpoint_number = usb_pcap_endpoint_number.UsbPcapEndpointNumber(self._io)
                self.transfer_type = KaitaiStream.resolve_enum(Usbpcap.Header.HeaderMain.TransferType, self._io.read_u1())
                self.data_size = self._io.read_u4le()
                _on = self.transfer_type
                if _on == Usbpcap.Header.HeaderMain.TransferType.isochronous:
                    self._raw_additional_header = self._io.read_bytes_full()
                    _io__raw_additional_header = KaitaiStream(BytesIO(self._raw_additional_header))
                    self.additional_header = Usbpcap.Header.HeaderMain.IsochHeader(_io__raw_additional_header, self, self._root)
                elif _on == Usbpcap.Header.HeaderMain.TransferType.control:
                    self._raw_additional_header = self._io.read_bytes_full()
                    _io__raw_additional_header = KaitaiStream(BytesIO(self._raw_additional_header))
                    self.additional_header = Usbpcap.Header.HeaderMain.ControlHeader(_io__raw_additional_header, self, self._root)
                else:
                    self.additional_header = self._io.read_bytes_full()

            class Info(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.reserved = self._io.read_bits_int_be(7)
                    self.pdo_to_fdo = self._io.read_bits_int_be(1) != 0


            class IsochHeader(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.start_frame = self._io.read_u8le()
                    self.packet_count = self._io.read_u8le()
                    self.error_count = self._io.read_u8le()
                    self.packet = Usbpcap.Header.HeaderMain.IsochHeader.IsochPacket(self._io, self, self._root)

                class IsochPacket(KaitaiStruct):
                    def __init__(self, _io, _parent=None, _root=None):
                        self._io = _io
                        self._parent = _parent
                        self._root = _root if _root else self
                        self._read()

                    def _read(self):
                        self.offset = self._io.read_u8le()
                        self.size = self._io.read_u8le()
                        self.status = usbd_status_windows.UsbdStatusWindows(self._io)



            class ControlHeader(KaitaiStruct):

                class Stage(Enum):
                    setup = 0
                    data = 1
                    status = 2
                    complete = 3
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.stage = KaitaiStream.resolve_enum(Usbpcap.Header.HeaderMain.ControlHeader.Stage, self._io.read_u1())




    @property
    def available_size(self):
        if hasattr(self, '_m_available_size'):
            return self._m_available_size if hasattr(self, '_m_available_size') else None

        self._m_available_size = (self._io.size() - self.header.header_size)
        return self._m_available_size if hasattr(self, '_m_available_size') else None

    @property
    def is_truncated(self):
        if hasattr(self, '_m_is_truncated'):
            return self._m_is_truncated if hasattr(self, '_m_is_truncated') else None

        self._m_is_truncated = self.header.header_main.data_size > self.available_size
        return self._m_is_truncated if hasattr(self, '_m_is_truncated') else None

    @property
    def data_size(self):
        if hasattr(self, '_m_data_size'):
            return self._m_data_size if hasattr(self, '_m_data_size') else None

        self._m_data_size = (self.available_size if self.is_truncated else self.header.header_main.data_size)
        return self._m_data_size if hasattr(self, '_m_data_size') else None


