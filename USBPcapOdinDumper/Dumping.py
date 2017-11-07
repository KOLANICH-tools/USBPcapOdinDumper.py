from Pipeline import Stage
from RichConsole import groups


class Dumping(Stage({"isUseful", "transformPacket", "generateName"})):
	def isUseful(dumper, packet):
		return True

	def transformPacket(dumper, packet):
		return packet

	def generateName(dumper, packet):
		packet.name = groups.Fore.blue(str(packet.index))

	def getPackets(dumper, fileName):
		raise NotImplementedError("Implement this shit!")
