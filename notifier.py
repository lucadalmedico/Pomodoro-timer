import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify, GdkPixbuf
import subprocess; 

class Notifier():
	def __init__(self, alarm):
		Notify.init("Pomodoro Timer")

		#type of notifications
		self.options = {'start' : self.__PomodoroStart,
						'short break' : self.__ShortBreak,
						'long break' : self.__LongBreak,}

		self.icon = GdkPixbuf.Pixbuf.new_from_file("./res/icon.png")

		self.alarm = alarm

	def notify(self,string):
		self.options[string]()
	
	def __show(self, notification):
		#add icon to the notification
		notification.set_icon_from_pixbuf(self.icon)
		notification.set_image_from_pixbuf(self.icon)
		
		notification.show()
		if self.alarm:
			#play an alarm sound
			subprocess.call(['/usr/bin/canberra-gtk-play',
				'--id','message'])

	def __PomodoroStart(self):
		"""
		Notify the beginning of the working session
		"""
		notification = Notify.Notification.new(
		"Pomodoro started",
		"Time to work!"
		)
		self.__show(notification)

	def __ShortBreak(self):
		"""
		Notify the beginning of the short break
		"""
		notification = Notify.Notification.new(
		"Pomodoro ended",
		"Enjoy a short break"
		)
		self.__show(notification)

	def __LongBreak(self):
		"""
		Notify the beginning of the long break
		"""
		notification = Notify.Notification.new(
		"Pomodoro ended",
		"Relax, you can have a long break"
		)
		self.__show(notification)