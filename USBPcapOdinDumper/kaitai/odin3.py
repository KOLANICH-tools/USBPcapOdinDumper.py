from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import IntEnum
if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception('Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s' % kaitaistruct.__version__)

class Odin3(KaitaiStruct):
    """[Samsung Odin](https://en.wikipedia.org/wiki/Odin_(firmware_flashing_software)) is a proprietary piece of software developed by Samsung and used to flash firmware into Samsung devices. Odin utility has a Loke counterpart in the device bootloader. This ksy documents the message format of the protocol they talk to each other.
    The protocol was reverse engineered by Benjamin Dobell who have created a MIT-licensed utility Heimdall, on which source code this ksy is based.
    If you wanna test and augment this spec keep in mind that a lot of websites spreading leaked versions of Odin utility were created with the sole purpose of spreading malware glued with the tool. The most trustworthy website I know is the one belonging to chainfire, a well-known dev on Android scene.
    
    Examples of the packets can be downloaded by the links:
      * https://github.com/Benjamin-Dobell/Heimdall/files/1414758/ODIN_flash_capture.zip
      * https://lindi.iki.fi/lindi/I9195IXXU1AOB1/KTU84P.I9195IXXU1AOB1_upgrade_Kies3.2.15072_2_Windows7_x64.pcap
      * https://lindi.iki.fi/lindi/I9195IXXU1AOB1/AP_flash_odin3.10_Windows7_x64.pcap
      * https://lindi.iki.fi/lindi/I9195IXXU1AOB1/recovery_flash_heimdall_d0526a3b_Debian_x64.pcap
      * https://lindi.iki.fi/lindi/I9195IXXU1AOB1/recovery_flash_heimdall_d0526a3b_Debian_x64.try2.pcap
      * https://lindi.iki.fi/lindi/I9195IXXU1AOB1/recovery_flash_valgrind_heimdall_d0526a3b_Debian_x64.pcap
    
    .. seealso::
       Source - https://github.com/Benjamin-Dobell/Heimdall/tree/master/heimdall/source
    
    
    .. seealso::
       Source - https://github.com/Samsung-Loki/Thor
    
    
    .. seealso::
       Source - https://github.com/nickelc/wuotan
    """

    class TrRequest(IntEnum):
        flash = 0
        dump = 1
        part = 2
        end = 3
        unknown2000 = 8192

    class ChipType(IntEnum):
        ram = 0
        nand = 1

    class PacketType(IntEnum):
        send_file_part = 0
        session = 100
        pit_file = 101
        file_transfer = 102
        end_session = 103
        device_information = 105

    class RebootValues(IntEnum):
        none = 0
        download = 1
        upload = 2
        charging_03 = 3
        fota = 4
        fota_bl = 5
        secure = 6
        normal = 7
        firmware_update = 8
        em_fuse = 9
        fota_setup = 11
        recovery_wd = 14
        factory = 15
        watch_reboot_mode = 16
        charging_11 = 17
        power_off_by_key = 18
        power_off_watch = 253

    class Destination(IntEnum):
        phone = 0
        modem = 1

    def __init__(self, is_loki_to_odin, was_previous_item_session_initiation, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.is_loki_to_odin = is_loki_to_odin
        self.was_previous_item_session_initiation = was_previous_item_session_initiation
        self._read()

    def _read(self):
        self.type = KaitaiStream.resolve_enum(Odin3.PacketType, self._io.read_u4le())
        _on = self.type
        if _on == Odin3.PacketType.device_information:
            self._raw_content = self._io.read_bytes_full()
            _io__raw_content = KaitaiStream(BytesIO(self._raw_content))
            self.content = Odin3.DeviceInformation(_io__raw_content, self, self._root)
        elif _on == Odin3.PacketType.end_session:
            self._raw_content = self._io.read_bytes_full()
            _io__raw_content = KaitaiStream(BytesIO(self._raw_content))
            self.content = Odin3.EndSession(_io__raw_content, self, self._root)
        elif _on == Odin3.PacketType.session:
            self._raw_content = self._io.read_bytes_full()
            _io__raw_content = KaitaiStream(BytesIO(self._raw_content))
            self.content = Odin3.Session(_io__raw_content, self, self._root)
        elif _on == Odin3.PacketType.file_transfer:
            self._raw_content = self._io.read_bytes_full()
            _io__raw_content = KaitaiStream(BytesIO(self._raw_content))
            self.content = Odin3.FileTransfer(_io__raw_content, self, self._root)
        elif _on == Odin3.PacketType.pit_file:
            self._raw_content = self._io.read_bytes_full()
            _io__raw_content = KaitaiStream(BytesIO(self._raw_content))
            self.content = Odin3.PitFile(_io__raw_content, self, self._root)
        else:
            self.content = self._io.read_bytes_full()

    class DeviceInformation(KaitaiStruct):
        """
        .. seealso::
           Source - https://github.com/Samsung-Loki/Thor/blob/18d655064b0a767c3b94d249385b77b536e2a582/TheAirBlow.Thor.Enigma/DeviceInfo.cs
        """

        class Type(IntEnum):
            model = 0
            serial = 1
            region = 2
            carrier = 3

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.signature = self._io.read_u4le()
            if not self.signature == 305419896:
                raise kaitaistruct.ValidationNotEqualError(305419896, self.signature, self._io, u'/types/device_information/seq/0')
            self.count = self._io.read_u4le()
            self.locations = [None] * self.count
            for i in range(self.count):
                self.locations[i] = Odin3.DeviceInformation.Location(self._io, self, self._root)
            self.info = [None] * self.count
            for i in range(self.count):
                self.info[i] = Odin3.DeviceInformation.Item(self._io, self, self._root)

        class Location(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.type = KaitaiStream.resolve_enum(Odin3.DeviceInformation.Type, self._io.read_u4le())
                self.offset = self._io.read_u4le()
                self.size = self._io.read_u4le()

        class Item(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.type = KaitaiStream.resolve_enum(Odin3.DeviceInformation.Type, self._io.read_u4le())
                self.size = self._io.read_u4le()
                self = self._io.read_bytes(self.size).decode(u'utf-8')

    class FileTransfer(KaitaiStruct):

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.request = KaitaiStream.resolve_enum(Odin3.TrRequest, self._io.read_u4le())
            _on = self.request
            if _on == Odin3.TrRequest.dump:
                self.content = Odin3.FileTransfer.Dump(self._io, self, self._root)
            elif _on == Odin3.TrRequest.part:
                self.content = Odin3.FileTransfer.Part(self._io, self, self._root)
            elif _on == Odin3.TrRequest.end:
                self.content = Odin3.FileTransfer.End(self._io, self, self._root)

        class FlashPart(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.sequence_byte_count = self._io.read_u4le()

        class Part(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.sequence_byte_count = self._io.read_u4le()
                self.part_index = self._io.read_u4le()

        class Dump(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.chip_type = KaitaiStream.resolve_enum(Odin3.ChipType, self._io.read_u4le())
                self.chip_id = self._io.read_u4le()

        class End(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.destination = KaitaiStream.resolve_enum(Odin3.Destination, self._io.read_u4le())
                self.sequence_byte_count = self._io.read_u4le()
                self.unknown1 = self._io.read_u4le()
                self.device_type = self._io.read_u4le()
                _on = self.destination
                if _on == Odin3.Destination.phone:
                    self.content = Odin3.FileTransfer.End.Phone(self._io, self, self._root)
                self.end_of_file = self._io.read_u4le()

            class Phone(KaitaiStruct):

                class File(IntEnum):
                    primary_bootloader = 0
                    pit = 1
                    secondary_bootloader = 3
                    secondary_bootloader_backup = 4
                    kernel = 6
                    recovery = 7
                    tablet_modem = 8
                    modem = 11
                    unknown12 = 18
                    efs = 20
                    param_lfs = 21
                    factory_file_system = 22
                    database_data = 23
                    cache = 24

                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self._read()

                def _read(self):
                    self.file_identifier = KaitaiStream.resolve_enum(Odin3.FileTransfer.End.Phone.File, self._io.read_u4le())

    class PitFile(KaitaiStruct):

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.request = KaitaiStream.resolve_enum(Odin3.TrRequest, self._io.read_u4le())
            _on = self.request
            if _on == Odin3.TrRequest.part:
                self.content = Odin3.PitFile.Part(self._io, self, self._root)
            elif _on == Odin3.TrRequest.end:
                self.content = Odin3.PitFile.End(self._io, self, self._root)

        class FlashPart(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.part_size = self._io.read_u4le()

        class Part(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.part_index = self._io.read_u4le()

        class End(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.file_size = self._io.read_u4le()

    class EndSession(KaitaiStruct):

        class Request(IntEnum):
            end_session = 0
            reboot_os = 1
            reboot_bootloader = 2
            power_off = 3

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.request = KaitaiStream.resolve_enum(Odin3.EndSession.Request, self._io.read_u4le())

    class Session(KaitaiStruct):
        """
        .. seealso::
           Source - https://github.com/Samsung-Loki/samsung-docs/blob/main/docs/Odin/Session.md
        """

        class Request(IntEnum):
            begin_session = 0
            device_type = 1
            total_bytes = 2
            set_oem_state = 3
            no_oem_check = 4
            file_part_size = 5
            erase_user_data = 7
            enable_tflash = 8
            set_region = 9
            enable_rtn = 10

        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.quirky_session = Odin3.Session.QuirkySession(self._io, self, self._root)
            self.regular_session = Odin3.Session.RegularSession(self._io, self, self._root)

        class RegularSession(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.request = KaitaiStream.resolve_enum(Odin3.Session.Request, self._io.read_u4le())
                _on = self.request
                if _on == Odin3.Session.Request.begin_session:
                    self.content = Odin3.Session.BeginSession(self._io, self, self._root)
                elif _on == Odin3.Session.Request.total_bytes:
                    self.content = Odin3.Session.TotalBytes(self._io, self, self._root)
                elif _on == Odin3.Session.Request.file_part_size:
                    self.content = Odin3.Session.FilePartSize(self._io, self, self._root)
                elif _on == Odin3.Session.Request.set_region:
                    self.content = Odin3.Session.SetRegion(self._io, self, self._root)

        class TotalBytes(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.total_bytes = self._io.read_u4le()

        class BeginSession(KaitaiStruct):
            """
            .. seealso::
               Source - https://github.com/Samsung-Loki/samsung-docs/blob/bc1e3a75dabf0c548bf50e2bf612d983c6f0bd8b/docs/Odin/Session.md
            """

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.protocol_version = self._io.read_u4le()

        class SetRegion(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.region = self._io.read_bytes(3).decode(u'ascii')

        class QuirkySession(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.content = Odin3.Session.BeginSession(self._io, self, self._root)

            @property
            def request(self):
                if hasattr(self, '_m_request'):
                    return self._m_request if hasattr(self, '_m_request') else None
                self._m_request = Odin3.Session.Request.begin_session
                return self._m_request if hasattr(self, '_m_request') else None

        class FilePartSize(KaitaiStruct):

            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self._read()

            def _read(self):
                self.file_part_size = self._io.read_u4le()

        @property
        def is_quirky_session_response(self):
            if hasattr(self, '_m_is_quirky_session_response'):
                return self._m_is_quirky_session_response if hasattr(self, '_m_is_quirky_session_response') else None
            self._m_is_quirky_session_response = self._root.is_loki_to_odin and self._root.was_previous_item_session_initiation
            return self._m_is_quirky_session_response if hasattr(self, '_m_is_quirky_session_response') else None

        @property
        def session(self):
            """Who have designed this shit?."""
            if hasattr(self, '_m_session'):
                return self._m_session if hasattr(self, '_m_session') else None
            self._m_session = self.quirky_session if self.is_quirky_session_response else self.regular_session
            return self._m_session if hasattr(self, '_m_session') else None

    @property
    def odin_handshake_message(self):
        if hasattr(self, '_m_odin_handshake_message'):
            return self._m_odin_handshake_message if hasattr(self, '_m_odin_handshake_message') else None
        self._m_odin_handshake_message = self._io.read_bytes(5)
        return self._m_odin_handshake_message if hasattr(self, '_m_odin_handshake_message') else None

    @property
    def loke_handshake_message(self):
        if hasattr(self, '_m_loke_handshake_message'):
            return self._m_loke_handshake_message if hasattr(self, '_m_loke_handshake_message') else None
        self._m_loke_handshake_message = self._io.read_bytes(4)
        return self._m_loke_handshake_message if hasattr(self, '_m_loke_handshake_message') else None
