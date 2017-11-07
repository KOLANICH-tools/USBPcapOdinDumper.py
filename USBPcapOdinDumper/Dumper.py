import os
from collections import OrderedDict
from glob import glob
from io import BytesIO

from Pipeline import *
from RichConsole import groups


class PacketUselessException(Exception):
	pass


class Dumper(Pipeline({"pipeline"})):
	def dump(self, fileName: str):
		"""Dumps captured packets into separate files"""
		dirName = os.path.splitext(fileName)[0]
		if not os.path.isdir(dirName):
			if os.path.exists(dirName):
				raise Exception("The file with name " + groups.Back.lightcyanEx(dirName) + " is already exists, so we cannot create a dir with that name")
			else:
				os.mkdir(dirName)
		for packet in self(fileName):
			cleanName = packet.name.plain()
			ofn = os.path.join(dirName, cleanName)
			print(groups.Fore.lightgreenEx("writing " + groups.Back.lightyellowEx(packet.name) + "..."))
			with open(ofn, "wb") as of:
				of.write(packet.body)

	def pipeline(self, stage, packet):
		packet = stage.transformPacket(self, packet)
		stage.generateName(self, packet)
		if stage.isUseful(self, packet):
			#stage.generateName(self, packet)
			return packet
		else:
			raise PacketUselessException("Packet " + packet.name + " is useless", packet)

	def __call__(self, fileName):
		packets = self.stages[0].getPackets(fileName)
		for packet in packets:
			try:
				(packet, stage) = self.pipeline(packet)
				yield packet
			except PipelineInterruptedException as ex:
				(args, kwargs, stage, ex) = ex.args
				(packet) = args
				if isinstance(stage, type):
					name = stage.__name__
				else:
					name = stage.__class__.__name__

				humanReadableStageName = name[: -len("Dumping")]

				if isinstance(ex, PacketUselessException):
					print(groups.Fore.yellow(groups.Fore.cyan(humanReadableStageName) + ": " + groups.Fore.blue(ex.args[1].index) + " considered useless"))
				else:
					raise ex
