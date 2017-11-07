__all__ = ("Packet",)


def packetPropRepr(o):
	if hasattr(o, "plain"):
		return o.plain()
	else:
		return repr(o)


class Packet:
	__slots__ = ("index", "meta", "body", "name")

	def __init__(self, **kwargs):
		for k in self.__class__.__slots__:
			setattr(self, k, None)
		for k, v in kwargs.items():
			setattr(self, k, v)

	def __repr__(self):
		return self.__class__.__name__ + "(" + ", ".join(((k + "=" + packetPropRepr(getattr(self, k))) for k in self.__class__.__slots__)) + ")"
