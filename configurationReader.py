import xml.etree.ElementTree

class Configuration():
	def __init__(self):
		#open the file ./res/configuration.xml
		self.file = xml.etree.ElementTree.parse \
			('./res/configuration.xml').getroot()

	def get_values(self):
		values = {}
		#read always the last configuration on the file
		values['pomodoro'] = int(self.file[-1].find('pomodoro').text)
		values['shortbreak'] = int(self.file[-1].find('shortbreak').text)
		values['longbreak'] = int(self.file[-1].find('longbreak').text)
		values['alarm'] = bool(self.file[-1].find('alarm').text == 'true')
		values['beforelongbreak'] = int(self.file[-1].find('beforelongbreak').text)

		return values