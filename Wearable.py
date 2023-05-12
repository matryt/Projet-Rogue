import Equipment


class Wearable(Equipment.Equipment):
	"""A wearable equipment."""
	def __init__(self, name, place, effect, abbrv="", usage=None):
		Equipment.Equipment.__init__(self, name, abbrv, usage)
		self.place = place
		self.effect = effect
