import time
import requests
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Path to chromedriver.exe
chromePath = ''' Insert chromedriver path '''

# Dictionary of class names [Might have to update depending on your code]
classes = {
	'page section' : 'rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t pfnyh3mw d2edcug0 ofv0k9yr cwj9ozl2',
	'section name' : 'a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7',
	'member name' : 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl oo9gr5id gpro0wi8 lrazzd5p',
	'join date' : 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 e9vueds3 j5wam9gi lrazzd5p m9osqain',
	'other info' : 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql rrkovp55 a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb mdeji52x sq6gx45u a3bd9o3v knj5qynh pipptul6 hzawbc8m'
}


# Completely loads all members of dynamically loading page
def scrollDown(driver):
	lastHeight = driver.execute_script("return document.body.scrollHeight")

	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		newHeight = driver.execute_script("return document.body.scrollHeight")

		if newHeight == lastHeight: break
		lastHeight = newHeight
	
	time.sleep(2)


class FacebookScraper:
	# Initializes Chrome driver (disables notifications pop up)
	def __init__(self, email, password, groupURL):
		option = Options()
		option.add_argument("--disable-infobars")
		option.add_argument("start-maximized")
		option.add_argument("--disable-extensions")
		option.add_experimental_option("prefs", { "profile.default_content_setting_values.notifications": 1 })

		self.user = email
		self.password = password
		self.URL = groupURL
		self.driver = webdriver.Chrome(chrome_options=option, executable_path=chromePath)


	# Logs into Facebook
	def login(self):
		self.driver.get('https://mbasic.facebook.com/login')

		search = self.driver.find_element_by_id('m_login_email')
		search.send_keys(self.user)

		search = self.driver.find_element_by_name('pass')
		search.send_keys(self.password, Keys.RETURN)

		time.sleep(1)


	# Gather names and join date of group members
	def getMemberDetails(self):
		self.__names = list()
		self.__joined = list()
		self.__other = list()
		
		self.driver.get(self.URL)
		time.sleep(2)

		scrollDown(self.driver)

		page = self.driver.page_source
		soup = BS(page, 'html.parser')

		# Gathers all sections of members page
		memberDivs = soup.find_all('div', classes['page section'])

		# Finds the section with all member info (ordered on join date)
		for section in memberDivs:
			crntSection = section.find('span', classes['section name'])
			if crntSection.text == 'New to the Group':
				all_members = section
				break
		
		# Finds all the member names/join dates and adds them to list
		nameDivs = all_members.find_all('a', classes['member name'])
		joinedDivs = all_members.find_all('span', classes['join date'])
		otherDivs = all_members.find_all('span', classes['other info'])
		for name, date, otherInfo in zip(nameDivs, joinedDivs, otherDivs): 
			self.__names.append(name.text)
			self.__joined.append( self._editDate(date.text) )
			self.__other.append( otherInfo.text if otherInfo.text else 'N/A' )

		time.sleep(2)


	# Parses out the dates into datetime objects
	# FB join date format include 'Joined about ... ago', 'Joined on ...', or 'Added by ... on ...'
	def _editDate(self, date):
		format_date = None

		if date.find('about ') >= 0:
			new_date = date[date.find('about ') + 6 :]

			# Number of days to push back for current day
			if new_date[ :new_date.find(' ')] == 'a': 
				num_day = 1
			else: 
				num_day = int(new_date[ :new_date.find(' ')])

			# Finds a possible date of joining (based off Facebook estimation)
			if new_date.find('weeks') >= 0: 
				format_date = datetime.now() - timedelta(days= 7 * num_day)
			else: 
				format_date = datetime.now() - timedelta(days= 30 * num_day)
		elif date.find('Joined on ') >= 0:
			new_date = date[date.find('Joined on ') + 10: ]
			today = datetime.today()
	
			if new_date == 'Monday': 		offset = (today.weekday()) % 7
			elif new_date == 'Tuesday': 	offset = (today.weekday() - 1) % 7
			elif new_date == 'Wednesday':	offset = (today.weekday() - 2) % 7
			elif new_date == 'Thursday':	offset = (today.weekday() - 3) % 7
			elif new_date == 'Friday': 		offset = (today.weekday() - 4) % 7
			elif new_date == 'Saturday': 	offset = (today.weekday() - 5) % 7
			else:							offset = (today.weekday() - 6)

			format_date = datetime.now() - timedelta(days=offset)
		else:
			format_date = datetime.strptime(date[date.find('on ') + 3:], '%B %d, %Y')
			
		return format_date
	

	# Returns number of members in group
	def countMembers(self):
		return len(self.__names)

	# Returns names list
	def getName(self, index):
		return self.__names[index]

	# Returns join date list
	def getJoined(self, index):
		return self.__joined[index].strftime('%B %d, %Y')

	# Returns other info list
	def getOther(self, index):
		return self.__other[index]

	# Quits out of driver
	def quit(self):
		self.driver.quit()


