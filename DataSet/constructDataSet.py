import random
import csv
from collections import OrderedDict

f = open('CSV_Database_of_Last_Names.csv','r')
LastNames = f.readlines()
f.close()

f = open('CSV_Database_of_First_Names.csv','r')
Names = f.readlines()
f.close()

f = open('areacodes.csv','r')
AreaCodes = f.readlines()
f.close()

f = open('streets.txt','r')
StreetNames = f.readlines()
f.close()

f = open('states.txt','r')
States = f.readlines()
f.close()

f = open('cities.csv','r')
Cities = f.readlines()
f.close()

f = open('zipCodes.csv','r')
ZipRanges = f.readlines()
f.close()

sampleSize = 10000

sample = []

attribute_sex = OrderedDict([
	(50,"male"),
	(100,"female")
])

attribute_age = OrderedDict([
	(7,"0,4"),
	(14,"5,9"),
	(21,"10,14"),
	(29,"15,19"),
	(37,"20,24"),
	(44,"25,29"),
	(50,"30,34"),
	(56,"35,39"),
	(62,"40,44"),
	(69,"45,49"),
	(76,"50,54"),
	(82,"55,59"),
	(87,"60,64"),
	(91,"65,69"),
	(94,"70,74"),
	(96,"75,79"),
	(98,"80,84"),
	(100,"85,105")
])

#https://en.wikipedia.org/wiki/Demography_of_the_United_States
attribute_race = OrderedDict([
	(1,"Native Hawaiian or Other Pacific Islander"),
	(2,"American Indian or Alaskan Native"),
	(7,"Asian American"),
	(14,"Other Race"),
	(27,"Black American"),
	(100,"White American")
])

attribute_hispanic = OrderedDict([
	("Native Hawaiian or Other Pacific Islander",0),
	("American Indian or Alaskan Native",23),
	("Asian American",2),
	("Other Race",97),
	("Black American",3),
	("White American",12)
])

#http://www.gnxp.com/blog/2008/12/nlsy-blogging-eye-and-hair-color-of.php
Hair_Colors = ["Light Blond", "Blond", "Light Brown", "Brown", "Black", "Red", "Grey"]
attribute_hair_color = OrderedDict([
	("Native Hawaiian or Other Pacific Islander",[0,0,0,50,100,0,0]),
	("American Indian or Alaskan Native",[0,0,0,50,100,0,0]),
	("Asian American",[0,0,0,25,100,0,0]),
	("Other Race",[0,1,4,50,99,100,0]),
	("Black American",[1,0,2,15,98,99,100]),
	("White American",[1,16,31,89,97,100,0])
])

Eye_Colors = ["Light Blue", "Blue", "Light Brown", "Brown", "Black", "Green", "Hazel", "Grey", "Other"]
attribute_eye_color = OrderedDict([
	("Native Hawaiian or Other Pacific Islander",[0,0,0,50,100,0,0,0,0]),
	("American Indian or Alaskan Native",[0,0,0,50,100,0,0,0,0]),
	("Asian American",[0,0,0,25,100,0,0,0,0]),
	("Other Race",[0,3,5,85,92,96,100,0,0]),
	("Black American",[0,1,2,86,98,98,100,0,0]),
	("White American",[1,35,36,69,70,83,98,99,100])
])

attribute_blood_type = OrderedDict([
	(1,"AB-"),
	(3,"B-"),
	(9,"A-"),
	(16,"O-"),
	(18,"AB+"),
	(27,"B+"),
	(63,"A+"),
	(100,"O+")
])

def generateAttribute(attList):
	rndm = random.randint(1,100)
	for distribution in attList:
		if (rndm <= distribution):
			return attList[distribution]
	return "N/A"

def generateDependentAttribute(parent,attList,attDist):
	rndm = random.randint(1,100)
	c = 0
	for distribution in attDist[parent]:
		if (rndm <= distribution):
			return attList[c]
		c = c+1
	return "N/A"
	
def generateAddress():
	address = []
	
	streetName = "Main St"
	streetNumber = random.randint(1000,9999)
	streetName = random.choice(StreetNames)
	address.append(str(streetNumber) + " " + streetName.strip('\n'))
	
	state = "Texas"
	state = random.choice(States).strip('\n')
	
	city = "Dallas"
	eligible = []
	for city in Cities:
		possible = city.split(',')
		if (possible[0] == state):
			eligible.append(possible[1].strip('\n'))
	address.append(random.choice(eligible))
	address.append(state)
	
	zipCode = "00000"
	for entry in ZipRanges:
		entryList = entry.split(',')
		if (entryList[0] == state):
				zipCode = random.randint(int(entryList[1]),int(entryList[2]))
	address.append(str(zipCode))
	
	return address

def generatePhone(state):
	phone = "817-555-5555"
	ac = "817"
	eligible = []
	for areacode in AreaCodes:
		possible = areacode.split(',')
		if (possible[0] == state):
			eligible.append(str(possible[1].strip('\n')))
	ac = random.choice(eligible)
	phone = ac + "-" + str(random.randint(100,999)) + "-" + str(random.randint(1000,9999))
	return phone

def generateAge():
	rndm = random.randint(1,100)
	for distribution in attribute_age:
		if (rndm <= distribution):
			ageRange = attribute_age[distribution].split(',')
			return str(random.randint(int(ageRange[0]),int(ageRange[1])))
	return "N/A"

def generateName():
	lastName = random.choice(LastNames).strip('\n')
	firstName = random.choice(Names).strip('\n')
	middleName = random.choice(Names).strip('\n')
	while(firstName == middleName):
		firstName = random.choice(Names).strip('\n')
		middleName = random.choice(Names).strip('\n')
	return [lastName, firstName, middleName]

def generateRace():
	rndm = random.randint(1,100)
	for distribution in attribute_race:
		if (rndm <= distribution):
			race = attribute_race[distribution]
			break
	rndm = random.randint(1,100)
	if (rndm <= attribute_hispanic[race]):
		hispanic = "1"
	else:
		hispanic = "0"
	return [race,hispanic]

def generateSSN():
	return str(random.randint(100,999)) + "-" + str(random.randint(10,99)) + "-" + str(random.randint(1000,9999))
	
def createObservation():
	#Name, Sex, Age, Ethnicity/Race, Hispanic/Latino, Hair Color, Eye Color, Address, City, State, Zip, Phone Number, Blood Type
	name = generateName() #Last Name, First Name, Middle Name
	sex = generateAttribute(attribute_sex)
	age = generateAge()
	race = generateRace() #Ethnicity/Race, Hispanic/Latino
	hair_color = generateDependentAttribute(race[0],Hair_Colors,attribute_hair_color)
	eye_color = generateDependentAttribute(race[0],Eye_Colors,attribute_eye_color)
	address = generateAddress() #Street, City, State, Zip
	phone = generatePhone(address[2])
	blood_type = generateAttribute(attribute_blood_type)
	ssn = generateSSN()
	
	return name[0] + "," + name[1] + "," + name[2] + "," + sex + "," + age + "," + race[0] + "," + race[1] + "," + blood_type + "," + hair_color + "," + eye_color + "," + address[0] + "," + address[1] + "," + address[2] + "," + address[3] + "," + phone + "," + ssn

print("Generating Sample...")

i = 0
while (i < sampleSize):
	sample.append(createObservation())
	i = i + 1

f = open('dataset.csv','w')
for observation in sample:
	f.write(observation + "\n")
f.close()
print("Sample Generated.")