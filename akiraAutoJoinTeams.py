from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import os.path
from os import path
import sys
from selenium.webdriver.common.action_chains import ActionChains
import requests

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_argument("--start-maximized")
opt.add_experimental_option("prefs", {
	"profile.default_content_setting_values.media_stream_mic": 1,
	"profile.default_content_setting_values.media_stream_camera": 1,
	"profile.default_content_setting_values.geolocation": 1,
	"profile.default_content_setting_values.notifications": 1
})

driver = None
URL = "https://teams.microsoft.com"

CREDS = {}
classname = ""


def send_msg(class_name, status):

	f = open("./assets/webhookurl.txt", "r")
	line = f.readlines()
	webhook_url = line[0]
	f.close()

	if status == "joined":

		content = "\n\
	 ```\n\
[SUCCESS !]\n\
| You joined " + str(class_name.replace("\n", "")) + " successfully ! |```"

	elif status == "noclass":

		content = "\n\
	 ```\n\
[FAILED !]\n\
| There is no class for the moment! |```"

	payload = {
		"content": content
	}

	f = open("./assets/discordnotifstatus.txt", "r")
	l = f.readlines()
	if l[0] == "1":
		requests.post(webhook_url, data=payload)
	elif l[0] == "0":
		print("\n            Discord notifications are disabled.")
	f.close()


def login():
	global driver
	global classname

	global CREDS
	print("logging in")
	emailField = driver.find_element_by_xpath('//*[@id="i0116"]')
	emailField.click()
	emailField.send_keys(CREDS['email'])
	driver.find_element_by_xpath(
		'//*[@id="idSIButton9"]').click() 
	time.sleep(4)
	passwordField = driver.find_element_by_xpath('//*[@id="i0118"]')
	passwordField.click()
	passwordField.send_keys(CREDS['passwd'])
	driver.find_element_by_xpath(
		'//*[@id="idSIButton9"]').click()
	time.sleep(5)
	driver.find_element_by_xpath(
		'//*[@id="idSIButton9"]').click() 
	time.sleep(5)
	joinclass(classname)


def joinclass(class_name):

	global driver

	f = open("./assets/lg.txt", "r")
	l = f.readlines()
	if l[0] == "fr":
		btntitledesaccam = "Désactiver la caméra"
		btntitledesacmic = "Désactiver le micro"
	elif l[0] == "eng":
		btntitledesaccam = "Turn camera off"
		btntitledesacmic = "Mute microphone"
	else:
		print("\n            Empty lg.txt or bad langage. Please retry.")
	f.close()

	time.sleep(5)
	classes_available = driver.find_elements_by_class_name("name-channel-type")

	for i in classes_available:
		if class_name.lower() in i.get_attribute('innerHTML').lower():
			print("JOINING CLASS ", class_name)
			i.click()
			break

	time.sleep(5)

	try:
		joinbtn = driver.find_element_by_class_name("ts-calling-join-button")
		joinbtn.click()

	except:
		k = 1
		while(k <= 15):
			print("Join button not found, trying again")
			time.sleep(60)
			driver.refresh()
			joinclass(class_name)
			k += 1
		print("Seems like there is no class today.")
		send_msg(class_name=class_name, status="noclass")

	time.sleep(4)
	webcam = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[2]/toggle-button[1]/div/button/span[1]')
	if webcam.get_attribute('title') == str(btntitledesaccam):
		webcam.click()

	time.sleep(3)

	microphone = driver.find_element_by_xpath('//*[@id="preJoinAudioButton"]/div/button/span[1]')
	if microphone.get_attribute('title') == str(btntitledesacmic):
		microphone.click()

	time.sleep(6)
	joinnowbtn = driver.find_element_by_xpath('//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
	joinnowbtn.click()

	send_msg(class_name=class_name, status="joined")


def start_browser():

	global driver

	driver = webdriver.Chrome(options=opt, service_log_path='NUL')

	driver.get(URL)

	WebDriverWait(driver, 10000).until(
		EC.visibility_of_element_located((By.TAG_NAME, 'body')))

	if "login.microsoftonline.com" in driver.current_url:
		login()


def startBot():

	global CREDS
	global classname

	f = open("./assets/logsmemory.txt", "r")
	for lines in f:
		emailUser, passwdUser = lines.split(":")
	f.close()

	lstClasses = []
	f = open("./assets/classesdB.txt", "r")
	for classes in f:
		lstClasses.append(classes)
	for i in range(len(lstClasses)):
		print("\n           " + str(i) + " - " + str(lstClasses[i]))
	f.close()

	op = input("\n            Enter class index : ")
	verif = input("\n            Confirm? [Y/N]: ")
	if verif == "N":
		op = input("\n            Enter class name : ")
	elif verif == "Y":
		print("\n            Confirmed.")
	else:
		print("\n            Bad input. Please retry.")
		sys.exit()


	CREDS = {'email': emailUser, 'passwd': passwdUser}

	classname = lstClasses[int(op)]
	start_browser()


def clear():
	if os.name == "nt":
		os.system("cls")
	else:
		os.system("clear")


clear()


def terminalAff():
	print("\n\
			/-----------------------------------------\ \n\
			| 1 - Start bot.                          |\n\
			| 2 - Add a class to the data base        |\n\
			| 3 - Remove a class from the data base   |\n\
			| 4 - View the data base of classes       |\n\
			| 5 - Modify your creditentials of Teams  |\n\
			| 6 - View your creditentials of Teams    |\n\
			| 7 - Disable/Enable discord notification |\n\
			| 8 - Modify webhook's url                |\n\
			| 9 - Choose langage of the webpage       |\n\
			| 10 - Clear terminal                     |\n\
			| 11 - Exit                               |\n\
			\-----------------------------------------/")


terminalAff()

term = True

while term:
	choice = input("\n\
			root@akiraBot:$ ")
	if choice == "1":
		startBot()

	elif choice == "2":
		print("\n----------------------------------------------------------")
		f = open("./assets/classesdB.txt", "a")
		newClass = input("\n            New class: ")
		f.write(newClass + "\n")
		f.close()
		print("\n            Class added successfully")
		print("\n----------------------------------------------------------")

	elif choice == "3":
		print("\n----------------------------------------------------------")
		class2rm = input(
			"\n            Index of the class you want to remove: ")
		lstClasses = []
		f = open("./assets/classesdB.txt", "r")
		for classes in f:
			lstClasses.append(classes)
		f.close()
		lstClasses.pop(int(class2rm))
		f = open("./assets/classesdB.txt", "w")
		for c in lstClasses:
			f.write(c)
		f.close()
		print("\n            Class removed successfully")
		print("\n----------------------------------------------------------")

	elif choice == "4":
		print("\n----------------------------------------------------------")
		lstClasses = []
		f = open("./assets/classesdB.txt", "r")
		for classes in f:
			lstClasses.append(classes)
		for i in range(len(lstClasses)):
			print("\n           " + str(i) + " - " + str(lstClasses[i]))
		f.close()
		print("\n----------------------------------------------------------")

	elif choice == "5":
		print("\n----------------------------------------------------------")
		newUser = input("\n            E-mail: ")
		newPasswd = input("\n            Password: ")
		f = open("./assets/logsmemory.txt", "w")
		f.write(newUser + ":" + newPasswd)
		f.close()
		print("\n            Creds modified with success.")
		print("\n----------------------------------------------------------")

	elif choice == "6":
		f = open("./assets/logsmemory.txt", "r")
		for line in f:
			print("\n----------------------------------------------------------")
			print("\n            Your creds:")
			user, passwd = line.split(":")
			print("\n            Email: " + str(user))
			print("\n            Password: " + str(passwd))
			print("\n----------------------------------------------------------")

	elif choice == "7":
		print("\n----------------------------------------------------------")
		f = open("./assets/discordnotifstatus.txt", "r")
		for line in f:
			if line == "0":
				print("\n            Discord notifications are disabled.")
				statusE = input(
					"\n            Do you want to enable it? [Y/N]: ")
				st = True
			elif line == "1":
				print("\n            Discord notifications are enabled.")
				statusD = input(
					"\n            Do you want to disable it? [Y/N]: ")
				st = False
		f.close()
		f = open("./assets/discordnotifstatus.txt", "w")
		if st:
			if statusE == "Y":
				f.write("1")
				print("\n            Modifications saved.")
			else:
				f.write("0")
		elif st == False:
			if statusD == "Y":
				f.write("0")
				print("\n            Modifications saved.")
			else:
				f.write("1")
		f.close()
		print("\n----------------------------------------------------------")

	elif choice == "8":
		print("\n----------------------------------------------------------")
		newUrl = input("\n            New webhook's URL: ")
		f = open("./assets/webhookurl.txt", "w")
		f.write(newUrl)
		f.close()
		print("\n            Webhook modified.")
		print("\n----------------------------------------------------------")

	elif choice == "9":
		print("\n----------------------------------------------------------")
		f = open("./assets/lg.txt", "w")
		lgchoose = input("\n            Choose your langage [fr/eng]: ")
		f.write(lgchoose)
		f.close()
		print("\n            Modifications saved.")
		print("\n----------------------------------------------------------")

	elif choice == "10":
		clear()
		terminalAff()

	elif choice == "11":
		print("\n            Exiting...\n")
		term = False

	else:
		print("\n            Command not found. Please retry")
