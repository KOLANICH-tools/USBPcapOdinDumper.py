from RichConsole import groups, rsjoin

from .Dumping import Dumping


class USBPcapDumping(Dumping):
	def isUseful(self, packet):
		return bool(packet.body) and bool(packet.meta)

	def generateName(self, packet):
		if isinstance(packet.meta, Exception):
			packet.name += groups.Fore.red("_ERROR_USBPCAP")
		else:
			packet.name = rsjoin("_", (packet.name, groups.Fore.green(packet.meta.transfer_type.name), groups.Fore.lightblueEx("←" if packet.meta.endpoint_number.is_input else "→")))
		return packet

	def transformPacket(self, packet):
		packet.meta = packet.body.header
		packet.body = packet.body.data
		if hasattr(packet.meta, "header_main"):
			packet.meta = packet.meta.header_main
		return packet
