from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os,sys,datetime,getpass

# CURRENT FEATURES:
# -> basic login
# -> report, report saving to file with time and date mentioned if report is successfull
# -> add an ID, it's password and corresponding name
# -> basic logout
# -> login as, from the set of names
# -> logout as, from the set of names
# -> custom login,report and logout
# -> list of all ids
# -> help menu
# -> current status
#Your data transfer has been exceeded, Please contact the administrator
#
# TODO: Change Priorities which will in turn require me to turn the data from the ids to queues and then I will have to play around with placement in the queue
# TODO: Blacklist IDs
# TODO: RUN SCRIPT EVERY TIME THE LAPTOP WAKES UP AND EVERY 1 HOUR

def fetchData(ids,pwds,names):
	Ids = open("/Users/Htnamus/All Stuff/Programming Stuff/Logins/ids.ht",'r')
	file = Ids.read()
	UsrsPwds = file.split('\n#')
	for UsrPwd in UsrsPwds:
		ids.append(UsrPwd.split(' ')[0])
		pwds.append(UsrPwd.split(' ')[1])
		names.append(UsrPwd.split(' ')[2])
	Ids.close()

def updateData(ids,pwds,names):
	details = open("/Users/Htnamus/All Stuff/Programming Stuff/Logins/ids.ht",'w')
	details.write(ids[0] + ' ' + pwds[0] + ' ' + names[0] + '\n#')
	for i in range(1,len(names) - 1):
		details.write(ids[ i ] + ' ' + pwds[ i ] + ' ' + names[ i ] + '\n#')
	n = len(names) - 1
	details.write(ids[ n ] + ' ' + pwds[ n ] + ' ' + names[ n ])
	

def logInFullOn(ids,pwds,names):
	driver = webdriver.Chrome()
	status = 0
	for idNo,pwd,name in zip(ids,pwds,names):
		driver.get("https://10.100.56.55:8090/httpclient.html")
		username = driver.find_element_by_name('username')
		password = driver.find_element_by_name('password')
		username.send_keys(idNo)
		password.send_keys(pwd)
		password.send_keys(Keys.RETURN)
		WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,"xmp")))
		message = driver.find_element_by_id('msgDiv')
		msg = message.text
		if msg == 'You have successfully logged in':
			print('\n' + 'You have successfully LOGGED IN as ' + name + '\n')
			current = open("/Users/Htnamus/All Stuff/Programming Stuff/Logins/current.ht",'w')
			current.write(idNo + ' ' + pwd + ' ' + name + ' ' + str(datetime.datetime.now()))
			current.close()
			status = 1
			break;
		elif msg == 'You have reached Maximum Login Limit.':
			print(name + ': Maximum Login Limit reached ')
			status = -1
		elif msg == 'The system could not log you on. Make sure your password is correct':
			status = -2
			print(name + ': Incorrect Details')
		elif msg == 'Your data transfer has been exceeded, Please contact the administrator':
			status = -3
			print(name + ': Data transfer exceeded')
	driver.close()
	return status

def reportChecks(ids,pwds,names,userStatuses,curid):
	driver = webdriver.Chrome()
	for idNo,pwd,name in zip(ids,pwds,names):
		print(name + ': ',end = '')
		driver.get("https://10.100.56.55:8090/httpclient.html")
		username = driver.find_element_by_name('username')
		password = driver.find_element_by_name('password')
		username.send_keys(idNo)
		password.send_keys(pwd)
		password.send_keys(Keys.RETURN)
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "xmp")))
		message = driver.find_element_by_id('msgDiv')
		msg = message.text
		if msg == 'You have successfully logged in':
			if idNo == curid:
				print('Logged in on this Device')
			else:
				print('Open')
			userStatuses.append(1)
			logout = driver.find_element_by_id('logincaption')
			logout.click()
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "xmp")))
		elif msg == 'You have reached Maximum Login Limit.':
			print('Maximum Login Limit Reached')
			userStatuses.append(-1)
		elif msg == 'The system could not log you on. Make sure your password is correct':
			print(' Incorrect Details')
			userStatuses.append(-2)
		elif msg == 'Your data transfer has been exceeded, Please contact the administrator':
			print('Data Tranfer Limit exceeded')

	driver.close()
	current = open('/Users/Htnamus/All Stuff/Programming Stuff/Logins/current.ht','w')
	current.write('')
	current.close()

def customLogin(idNo, pwd,use): #use = 1 for normal login, use = 2 when logging in after logging out because of report
	driver = webdriver.Chrome()
	driver.get("https://10.100.56.55:8090/httpclient.html")
	username = driver.find_element_by_name('username')
	password = driver.find_element_by_name('password')
	username.send_keys(idNo)
	password.send_keys(pwd)
	password.send_keys(Keys.RETURN)
	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,"xmp")))
	message = driver.find_element_by_id('msgDiv')
	msg = message.text
	if msg == 'You have successfully logged in':
		if use == 1:
			ids, pwds, names = [ ], [ ], [ ]
			fetchData(ids, pwds, names)
			print('\n' + 'You have successfully LOGGED IN' + '\n')
			current = open("/Users/Htnamus/All Stuff/Programming Stuff/Logins/current.ht",'w')
			current.write(idNo + ' ' + pwd + ' ' + names[ids.index(idNo)] + ' ' + str(datetime.datetime.now()))
			current.close()
		if use == 2:
			ids, pwds, names = [],[],[]
			fetchData(ids,pwds,names)
			print('\nYou remain to be logged in as ' + names[ids.index(idNo)],end = '\n\n')
			current = open("/Users/Htnamus/All Stuff/Programming Stuff/Logins/current.ht", 'w')
			current.write(idNo + ' ' + pwd +  ' ' + names[ids.index(idNo)])
			current.close()
		return 1
	elif msg == 'You have reached Maximum Login Limit.':
		print('Maximum Login Limit Reached')
		return -1
	elif msg == 'The system could not log you on. Make sure your password is correct':
		print('Incorrect Details')
		return -2
	elif msg == 'Your data transfer has been exceeded, Please contact the administrator':
		print('Data transfer limit exceeded')
		return -3
	driver.close()

def customReport(idNo,pwd):
	driver = webdriver.Chrome()
	driver.get("https://10.100.56.55:8090/httpclient.html")
	username = driver.find_element_by_name('username')
	password = driver.find_element_by_name('password')
	username.send_keys(idNo)
	password.send_keys(pwd)
	password.send_keys(Keys.RETURN)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "xmp")))
	message = driver.find_element_by_id('msgDiv')
	msg = message.text
	if msg == 'You have successfully logged in':
		print('\n' + 'This ID is open' + '\n')
		logout = driver.find_element_by_id('logincaption')
		logout.click()
		return 1
	elif msg == 'You have reached Maximum Login Limit.':
		print('Maximum Login Limit Reached')
		return -1
	elif msg == 'The system could not log you on. Make sure your password is correct':
		print('Incorrect Details')
		return -2
	elif msg == 'Your data transfer has been exceeded, Please contact the administrator':
		print('Data transfer limit exceeded')
		return -3
	driver.close()

def logout(idNo,pwd,use):
	driver = webdriver.Chrome()
	driver.get("https://10.100.56.55:8090/httpclient.html")
	username = driver.find_element_by_name('username')
	password = driver.find_element_by_name('password')
	username.send_keys(idNo)
	password.send_keys(pwd)
	password.send_keys(Keys.RETURN)
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "xmp")))
	message = driver.find_element_by_id('msgDiv')
	msg = message.text
	if msg == 'You have successfully logged in':
		logout = driver.find_element_by_id('logincaption')
		logout.click()
		print('\nLOGGED OUT\n')
		return 1
	elif msg == 'You have reached Maximum Login Limit.':
		print('NOT LOGGED IN ON THIS SYSTEM')
		return -1
	elif msg == 'The system could not log you on. Make sure your password is correct':
		if use == 1:
			print('ERROR: Try logging in again and then logging out')
		elif use == 2:
			print('ERROR: Incorrect details entered. Please try again')
		elif use == 3:
			print('ERROR: Incorrect details in Database. Please contact admin')
		return -2
	elif msg == 'Your data transfer has been exceeded, Please contact the administrator':
		print('Data transfer limit exceeded')
		return -3
	driver.close()

def priorityChange():
	ids,pwds,names = [],[],[]
	fetchData(ids,pwds,names)
	print('\n The following are the names in the priority order:\n')
	for name,pos in zip(names,range(1,len(names)+1)):
		print( '\t' + str(pos) + ': ' + name,end='\n')
	print('\n')
	choice = input('Would you like to change the priorities(y/n):\nChoice:')
	if choice == 'y' or choice == 'Y':
		detail = int(input('Would you like to(1/2):\n\t1. Enter all the names in the new order\n\t2.Interchange priorities\nChoice:'))
		if detail not in [1,2]:
			print('Incorrect input. Please try again')
		elif detail == 1:
			print('Enter the new priority order below')
			newNames = []
			newIDs = []
			newPwds = []
			for count in range(1,len(names)+1):
				newName = input(str(count) + ':')
				tries = 0
				while newName in newNames or newName not in names or tries < 3:
					tries += 1
					if newName in newNames:
						print('Name has been mentioned before. Try another name')
					if newName not in names:
						print('Details of this person are not available. Try the name of a person in the above list')
					newName = input(str(count) + ':')
				newNames.append(newName)
				newIDs.append(ids[names.index(newName)])
				newPwds.append(pwds[names.index(newName)])
			updateData(newIDs,newPwds,newNames)
			print('NEW PRIORITY ORDER:\n')
			for name,count in zip(newNames,range(1,len(newNames)+1)):
				print('\t' + str(count) + ':' + name)
			print('\n')
		elif detail == 2:
			print('Enter the serial numbers of the names you\'d like to interchange:\n')
			sno1 = int(input('Serial Number 1: ')) - 1
			sno2 = int(input('Serial Number 2: ')) - 1
			if sno1 > len(names) or sno2 > len(names):
				print('ERROR: Serial number out of bounds.')
			else:
				tempId = ids[sno1]
				tempName = names[sno1]
				tempPwd = pwds[sno1]
				ids[sno1] = ids[sno2]
				names[sno1] = names[sno2]
				pwds[sno1] = pwds[sno2]
				ids[sno2] = tempId
				names[sno2] = tempName
				pwds[sno2] = tempPwd
				updateData(ids,pwds,names)
				print('NEW PRIORITY ORDER:\n')
				for name, count in zip(names, range(1, len(names) + 1)):
					print('\t' + str(count) + ':' + name)
				print('\n')
	elif choice != 'n' and choice != 'N':
		print('Incorrect input. Please try again')

ids, pwds, names = [],[],[]
commands = ['login','report','help','--help','add','current','logout',' logout as','login as','custom','custom report','custom login','custom logout','list','priority']
args = 0
for arg in sys.argv:
	if arg in commands:
		args += 1
if len(sys.argv) == 1 or args==0:
	print('\nERROR: Argument not found. Try \'jaffa help\'\n')
elif 'help' in sys.argv or '--help' in sys.argv :
	print('\nJAFFA HELP:')
	print('\njaffa is a command-line assistant to login into Cyberroam on DAIICT Campus\n')
	print('SYNTAX:\n\n\tjaffa <arg1> <arg2> <arg3> ...\n\n\t\t\tOR\n\n\tcbr <arg1> <arg2> <arg3> ...\n\n\t\t\tOR\n\n\tcyberroam <arg1> <arg2> <arg3> ...\n')
	print('Usable Arguments:\n')
	print('\tlogin - logs into an id based on the set priority order\n')
	print('\treport - gives a status report of all the IDs and logs in if previously logged in\n')
	print('\tadd - add a ID, it\'s password and corresponding name\n')
	print('\tlist - gives a list of all available IDs and their corresponding names\n')
	print('\tcurrent - gives the current status and the id if logged in( through jaffa only)\n')
	print('\tlogout - logs out of the ID logged in with( through jaffa only)\n')
	print('\tlogin as - log in through a specific name. Type \'I dunno\' for list of names\n')
	print('\tlogout as - logout through a specific name. Type \'I dunno\' for list of names\n')
	print('\tcustom - suffix or prefix to login,logout or/and report. Do the corressponding action with a supplied custom ID and password\n')
	print('\tpriority - change priorities\n')
	print('\thelp/--help - help(Duh??)')
	print('\n')
	print('NOTE: There must be at least one argument\n')
	print('\t\t\t\t\t\t\t\t\t-by htnamuS\n')

elif 'add' in sys.argv:
	details = open('/Users/Htnamus/All Stuff/Programming Stuff/Logins/ids.ht','a')
	details.write('\n')
	id = '#' + str(input('Enter your ID number:'))
	pwd = str(getpass.getpass('Enter your password:'))
	name = str(input('Enter your name:'))
	details.write(id + ' ' + pwd + ' ' + name)
	details.close()

elif 'current' in sys.argv:
	current = open('/Users/Htnamus/All Stuff/Programming Stuff/Logins/current.ht','r')
	curUser = current.readline().split(' ')
	current.close()
	if curUser != ' ' and curUser != '' and len(curUser) != 0:
		curId = curUser[0]
		curUsr = curUser[2]
		curDate = curUser[3]
		curTime = curUser[4]
		print('\nLogged in as ' + curUsr + ' using ID: ' + curId + ' at ' + curTime + ' on ' + curDate, end = '\n\n')
	else:
		print('\nNo ID is logged in\n\n')

elif 'logout' in sys.argv:
	current = open('/Users/Htnamus/All Stuff/Programming Stuff/Logins/current.ht','r')
	details = current.readline()
	id = details.split(' ')[0]
	pwd = details.split(' ')[1]
	print('Logging out ...')
	logout(id, pwd,1) # use = 1 for automatic logout; 2 for custom logout(can have incorrect details;3 for logout from list
	current = open('/Users/Htnamus/All Stuff/Programming Stuff/Logins/current.ht', 'w')
	current.write('')
	current.close()

elif 'list' in sys.argv:
	ids,pwds,names = [],[],[]
	fetchData(ids,pwds,names)
	print(' ')
	for id,name in zip(ids,names):
		print(name + ': ' + id)

elif 'priority' == sys.argv[1]:
	priorityChange()

elif len(sys.argv) > 2 and 'logout' in sys.argv and 'as' == sys.argv[sys.argv.index('logout') + 1]:
	ids, pwds, names = [ ], [ ], [ ]
	fetchData(ids, pwds, names)
	name = input(' Enter the name of the person you want to logout as: (or enter "I dunno" for the list of names)\n')
	if name == 'I dunno':
		for name in names:
			print(str(names.index(name) + 1) + '. ' + name)
		name = input('Enter a name: (case-sensitive)\n')
	if name not in names:
		print('ERROR: The name isn\'t present in the list of IDs\nTry jaffa add')
		exit()
	else:
		print('Logging out ...')
		logout(ids[ names.index(name) ], pwds[ names.index(name) ],3)

elif len(sys.argv) > 2 and 'login' in sys.argv and 'as' == sys.argv[sys.argv.index('login') + 1]:
	ids, pwds, names = [],[],[]
	fetchData(ids,pwds,names)
	name = input(' Enter the name of the person you want to login as: (or enter "I dunno" for the list of names)\n')
	if name == 'I dunno':
		for name in names:
			print(str(names.index(name)+1) + '. ' + name)
		name = input('Enter a name: (case-sensitive)\n')
	if name not in names:
		print('ERROR: The name isn\'t present in the list of IDs\nTry jaffa add')
		exit()
	else:
		print('Logging in ...')
		customLogin(ids[names.index(name)],pwds[names.index(name)],1)

elif 'custom' in sys.argv:
	idNo = str(input('Enter your ID:'))
	pwd = getpass.getpass('Password:')
	if 'logout' in sys.argv:
		print('Logging out')
		logout(idNo,pwd,2)
	elif 'login' in sys.argv or 'report' in sys.argv:
		if 'login' in sys.argv:
			print('Logging in ...')
			customLogin(idNo,pwd,1)
		if 'report' in sys.argv:
			print('Checking status ...')
			customReport(idNo,pwd)
	else:
		print('ERROR: custom is a prefix/suffix. Enter main argument. Enter \'jaffa help\' for help')
else:
	if 'report' in sys.argv:
		print('Generating report ...')
		userStatuses = []
		fetchData(ids, pwds, names)
		current = open('/Users/Htnamus/All Stuff/Programming Stuff/Logins/current.ht', 'r')
		curDetails = current.readline()
		current.close()
		details = curDetails.split(' ')
		curid = details[ 0 ]
		curpwd = details[ 1 ]
		reportChecks(ids,pwds,names,userStatuses,curid)
		report = open('/Users/Htnamus/All Stuff/Programming Stuff/Logins/report.ht', 'a')
		report.write('REPORT OF ' + str(datetime.datetime.now()) + ': \n')
		for name,status in zip(names,userStatuses):
			report.write('\n' + name )
			if status == 1:
				report.write(' OPEN')
			elif status ==-1:
				report.write(' MAXIMUM LOGIN LIMIT REACHED')
			elif status == -2:
				report.write(' INCORRECT DETAILS')
			else:
				report.write(' ERROR')

		report.write('\n\n')
		report.close()
		if curDetails != ' ' and curDetails != '' and len(curDetails) != 0:
			customLogin(curid,curpwd,2)
	if 'login' in sys.argv:
		print('Logging in ...')
		fetchData(ids,pwds,names)
		status = logInFullOn(ids,pwds,names)
		#STATUSES:
		# 0 stands for process started not logged in yet
		# 1 stands for logged in successfully
		# -1 stands for maximum login limit
		# -2 stands for incorrect details
		if status < 0 :
			print('\n Unable to login with any ID\n')
		elif status == 0 :
			print('Unknown error. Unable to traverse through IDs')
