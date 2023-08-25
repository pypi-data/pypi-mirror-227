from threading import Thread
from shedok.shedule import Shedule
import time

class Sheduler:
	def __init__(self):
		self.shedules = []
		self.thread = None
		self.alive = False

	def add(self, shedule: Shedule):
		self.shedules.append(shedule)

	def tick(self):
		for shedule in self.shedules:
			shedule()

	def run(self):
		self.alive = True
		def runtime():
			while self.alive:
				self.tick()

		self.thread = Thread(target=runtime)
		self.thread.start()

	def stop(self):
		self.alive = False