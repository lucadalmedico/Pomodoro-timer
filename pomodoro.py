from application import PomodoroTimer
import sys

try:
	app = PomodoroTimer()
	app.mainloop()
except:
	print "Unexpected error:", sys.exc_info()[0]
	raise