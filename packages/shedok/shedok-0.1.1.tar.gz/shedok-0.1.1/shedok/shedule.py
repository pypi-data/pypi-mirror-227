import random, datetime

class Shedule:
	def __init__(self, func, time, *args, **kwargs):
		self.id = random.randint(-1e9, 1e9)
		self.func = func
		self.time = time
		self.args = args
		self.kwargs = kwargs
		self.executed = False

	def __call__(self, when=None):
		if when is None:
			when = datetime.datetime.now()
		if self.time <= when and not self.executed:
			self.executed = True
			self.func(*self.args, **self.kwargs)
