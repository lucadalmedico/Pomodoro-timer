#!/usr/bin/python
 
from Tkinter import *

from notifier import Notifier

from configurationReader import Configuration


 
class PomodoroTimer(Frame):

	def __start(self):
		"""
		Start to work, this function is executed only the first
		time
		"""
		self.__button.config(text = "Stop",
			background = '#e21212',
			activebackground = '#f21515',
			command =  self.quit)
		

		self.__status.config(text='Work!')
		self.__pomodorolabel.config(text=('Number of pomodoros done: ' 
			+ str(self.__npomodoro)) )

		self.__working = True

		self.__notifier.notify('start')

		self.after(1000,self.__update)

	def __update(self):
		"""
		Keep updating the timer and change the session if ended
		"""
		self.__secs -= 1
		if self.__secs < 0:
			self.__mins -= 1
			self.__secs = 59
		
		if self.__mins == 0 and self.__secs ==0:
			if self.__working:
				self.__break()
				self.__working = False  
			elif not self.__working:
				self.__restart()
				self.__working = True

		self.__timeformat = '{:02d}:{:02d}'.format(self.__mins, 
			self.__secs)
		
		self.__clock.config(text = self.__timeformat)

		self.__clock.after(1000,self.__update)

	def __break(self):
		"""
		Start a short break or a long break every four session
		"""
		self.__secs = 0
		self.__npomodoro += 1
		self.__pomodorolabel.config(text=('Number of pomodoros done: ' 
			+ str(self.__npomodoro)) )
		self.__status.config(text='Break')

		if divmod(self.__npomodoro, self.__sprintsessions)[1] == 0:
			self.__notifier.notify('long break')
			self.__mins = self.__longbreaktime
		else:
			self.__notifier.notify('short break')
			self.__mins = self.__shortbreaktime

	def __restart(self):
		"""
		Restart the working session after a break
		"""
		self.__mins, self.__secs = self.__pomodorotime, 0
		self.__status.config(text='Work!')       

		self.__notifier.notify('start')
		
	def __createWidgets(self):
		"""
		Create all the widgets needed
		"""

		self.__buttons = Frame(self,
			bd = 0,
			bg = 'white')
		
		self.__button = Button(self,
			width=15, height=2,
			text = "Start",
			background = '#0ece10',
			activebackground = '#16e519',
			command = self.__start)
		
		#initialize minute and second for the timer
		self.__mins, self.__secs = self.__pomodorotime , 0
 
		self.__timeformat = '{:02d}:{:02d}'.format(self.__mins, 
			self.__secs)

		self.__clock = Label(self, font=('times', 50, 'bold'),
			background = 'white')   		

		self.__clock.config(text=self.__timeformat)  

		#display the number of session done
		self.__pomodorolabel = Label(self, font=(21),
			background = 'white')
 
		#display a description of the session
		self.__status = Label(self, font=('times', 18, 'bold'),
			background = 'white')    

		self.__buttons.pack(side = BOTTOM, fill = X)
		self.__button.pack(in_ = self.__buttons)
		self.__clock.pack( fill = BOTH, expand = 1)
		self.__status.pack(fill = BOTH, expand = 1)
		self.__pomodorolabel.pack(fill = BOTH, expand = 1)

	def __init__(self, master = Tk()):     
		Frame.__init__(self, master)

		configuration = Configuration().get_values()

		self.__pomodorotime = configuration['pomodoro'] #minute of work
		self.__shortbreaktime = configuration['shortbreak'] #minute of short break
		self.__longbreaktime = configuration['longbreak'] #minute of long break
		#number of session before a long break
		self.__sprintsessions = configuration['beforelongbreak'] 
		alarm = configuration['alarm']

		self.__npomodoro = 0 # number of session done
		self.__notifier = Notifier(alarm)
		self.__working = False

		self.master.title("Pomodoro Timer")
		self.master.minsize(230, 220)
		self.master.maxsize(400, 300)
		self.master.configure(background = 'white')

		self.master.tk.call('wm', 'iconphoto', self.master._w, 
			PhotoImage(file='./res/icon.png'))

		self.pack()
		self.__createWidgets()
