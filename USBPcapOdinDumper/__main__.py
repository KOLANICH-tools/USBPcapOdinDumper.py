import importlib
import os
import platform
import sys
from glob import glob

import colorama
from RichConsole import RichStr, groups

from .Dumper import Dumper
from .OdinDumping import OdinDumping
from .PcapDumping import PcapDumping
from .USBPcapDumping import USBPcapDumping

neededCharacters = "←→"
if __name__ == "__main__":
	import plumbum.cli

	class UnpackerCLI(plumbum.cli.Application):
		DESCRIPTION = r"""This shit unpacks usbpcap or usbmon .pcap files with odin3 protocol captures.It creates a directory for each file. If called without arguments, it processes all the pcap files in current folder. For the license see UNLICENSE file."""

		def main(self, *pcaps: plumbum.cli.ExistingFile):
			# sys.stdout = open('./res.txt','wt', encoding="utf-8")
			if platform.system() == "Windows":
				# colorama.init() # extremely glitchy
				try:
					bytes(neededCharacters, encoding=sys.stdout.encoding)
				except BaseException:
					print(groups.Fore.red("Your current console codepage (", groups.Fore.blue(sys.stdout.encoding), ") cannot show all the needed characters (", groups.Fore.green(repr(neededCharacters)), "). Type ", groups.Back.lightblackEx(groups.Fore.green("chcp"), " ", groups.Fore.blue("65001")), " to switch to ", groups.Fore.green("UTF-8")))
					return 1
			if not pcaps:
				pcaps = glob("./*.pcap")
			od = OdinDumping()
			dumper = Dumper([PcapDumping, USBPcapDumping, od])
			for fn in pcaps:
				od.__init__()
				print(RichStr("processing file ", groups.Fore.cyan(fn), " ..."))
				dumper.dump(fn)

	UnpackerCLI.run()
