
# Pending tasks management

LICENSE: The MIT License


## Requirements

- Python 3.7 or higher
- setuptools

## Usage

---

	import shedok

### Shedule

---

	shedok.Shedule(func, time, *args, **kwargs)  # Creates shedule
	shedok.Shedule.__call__(when=None) -> None  # Tries to execute task(once and if time <= when)

### Sheduler 

---
	
	shedok.Sheduler()  # Creates shedules manager
	shedok.Sheduler.add(shedule: Shedule)  # Adds task to manager
	shedok.Sheduler.tick()  # Calls every task
	shedok.Sheduler.run()  # Creates new thread, that tick() every time
	shedok.Sheduler.stop()  # Stops thread
