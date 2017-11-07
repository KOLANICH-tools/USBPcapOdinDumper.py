from RichConsole import groups

from .Dumping import Dumping
from .kaitai.pcap import *
from .Packet import Packet


class KaitaiPcapDumping(Dumping):
	def isUseful(dumper, packet):
		return bool(packet.body) and not isinstance(packet.meta, Exception)

	def getPackets(fileName):
		p = Pcap.from_file(fileName)
		for i, packet in enumerate(p.packets):
			if isinstance(packet.body, tuple):  # an error has occured
				yield Packet(index=i, meta=packet.body[0], body=packet.body[0])
			else:
				yield Packet(index=i, body=packet.body, name=groups.Fore.cyan(str(i)))

PcapDumping = KaitaiPcapDumping
