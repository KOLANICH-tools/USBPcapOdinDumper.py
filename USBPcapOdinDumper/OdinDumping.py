import re

from RichConsole import groups, rsjoin

from .Dumping import Dumping
from .kaitai.odin3 import *

from icecream import ic
from io import BytesIO
from kaitaistruct import KaitaiStream


class OdinDumping(Dumping):
	def __init__(self, *args, **kwargs):
		self.was_previous_item_session_initiation = False
		super().__init__(*args, **kwargs)

	def isUseful(self, dumper, packet):
		ic(packet)
		return packet.meta.transfer_type.name == "bulk" or len(packet.body) >= 1024 or packet.body == b"ODIN" or packet.body == b"LOKE"

	def transformPacket(self, dumper, pckt):
		return pckt

	invalidEnumRx = re.compile("^(.+) is not a valid (.+)$")

	def generateName(self, dumper, pckt):
		if pckt.body == b"ODIN" or pckt.body == b"LOKE":
			pckt.name = rsjoin("_", (pckt.name, str(pckt.body, encoding="ascii")))
		else:
			errorName = None
			try:
				with BytesIO(pckt.body) as f:
					o = Odin3(pckt.meta.endpoint_number.is_input, self.was_previous_item_session_initiation, KaitaiStream(f))
			except ValueError as error:
				self.was_previous_item_session_initiation = False

				errorName = "ENUM"
				m = self.__class__.invalidEnumRx.match(error.args[0])
				if m:
					(num, name) = m.groups()
					try:
						num = hex(int(num))
					except BaseException:
						pass
					errorName = rsjoin("_", (errorName, groups.Fore.lightblueEx(name), groups.Fore.cyan(num)))
			except Exception as error:
				self.was_previous_item_session_initiation = False

				errorName = ""
				print(groups.Fore.red(str(error)))
			else:
				self.was_previous_item_session_initiation = not pckt.meta.endpoint_number.is_input and o.type == Odin3.PacketType.session and o.content.regular_session.request == Odin3.Session.Request.begin_session

				if not isinstance(o.type, Odin3.PacketType):
					errorName = rsjoin("_", ("ENUM", groups.Fore.lightblueEx(Odin3.PacketType.__name__), groups.Fore.cyan(hex(o.type))))
				else:
					pckt.name = rsjoin("_", (pckt.name, o.type.name))
					if hasattr(o.content, "request"):
						pckt.name = rsjoin("_", (pckt.name, groups.Fore.green(str(o.content.request))))

			if errorName is not None:
				pckt.name = rsjoin("_", (pckt.name, groups.Fore.red(rsjoin("_", ("ERROR_ODIN3", errorName)))))
		return pckt
