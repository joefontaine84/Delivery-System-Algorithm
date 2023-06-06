# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

"""Your task is to determine an algorithm, write code, and present a solution where all 40 packages (listed in the attached “WGUPS Package File”)
will be delivered on time while meeting each package’s requirements and keeping the combined total distance traveled under 140 miles for both trucks.
The specific delivery locations are shown on the attached “Salt Lake City Downtown Map,” and distances to each location are given in the attached “WGUPS
Distance Table.” The intent is to use the program for this specific location and also for many other cities in each state where WGU has a presence.
As such, you will need to include detailed comments to make your code easy to follow and to justify the decisions you made while writing your scripts.
Keep in mind that the supervisor should be able to see, at assigned points, the progress of each truck and its packages by any of the variables listed
in the “WGUPS Package File,” including what has been delivered and at what time the delivery occurred.

Assumptions:
•   Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.

•   The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.

•   There are no collisions.

•   Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.

•   Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.

•   The delivery and loading times are instantaneous, i.e., no time passes while at a delivery or when moving packages to a truck at the hub (that time is factored into the calculation of the average speed of the trucks).

•   There is up to one special note associated with a package.

•   The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S State St., Salt Lake City, UT 84111) until 10:20 a.m.

•   The distances provided in the WGUPS Distance Table are equal regardless of the direction traveled.

•   The day ends when all 40 packages have been delivered."""
import datetime
import math


# Outline:

# (1) Create Class to represent package ... include package variables as are provided in the Excel Format

# (2) Create Class to represent trucks.... load packages onto each truck

# how to populate distances between hubs?

class Package:
    packageID = 0
    packageAddress = ""
    city = ""
    state = ""
    zipCode = 0
    deadline = datetime
    mass = 0
    specialNotes = ""
    status = ""

    def __init__(self, packageID, packageAddress, city, state, zipCode, deadline, mass, specialNotes):
        self.packageID = packageID
        self.packageAddress = packageAddress
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.deadline = deadline
        self.mass = mass
        self.specialNotes = specialNotes


class Truck:
    packageList = []
    destinations = []
    speedMPH = 18
    time = datetime
    name = ""

packageObjList = []  # list of all package objects
destinations = {}
startingPoint = "4001 South 700 East"
class HashTable:
    hashTable = {}  # blank hashtable (dictionary)
    for i in range(10):
        hashTable.__setitem__(i, [])

    # imports the WGUPS Package File
    import csv
    with open('WGUPS Package File.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        next(csvreader)  # skips over header row of CSV file
        for row in csvreader:
            packageObj = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                                 row[7])  # creates a package object

            if row[7].__contains__("delay"):
                packageObj.status = "Delayed"
            else:
                packageObj.status = "Ready for delivery"

            packageObjList.append(packageObj)
            bucket = int(packageObj.packageID) % 10  # determines which bucket to place the object in
            hashTable[bucket].append(packageObj)  # places the packageobj in the corresponding bucket


    def hashInsert(self, ID, address, deadline, city, zipcode, weight, status):
        packageObj = Package(ID, address, city, '', zipcode, deadline, weight,
                             '')  # the first blank variable is the "state" variable, and the second blank variable is the "special instructions"
        packageObj.status = status
        bucket = int(packageObj.packageID) % 10  # determines which bucket to place the object in
        self.hashTable[bucket].append(packageObj)  # places the packageobj in the corresponding bucket

    def hashLookUp(self, ID):
        tempVar = ID % 10
        print(tempVar)
        tempList = self.hashTable.get(tempVar)
        print(tempList)
        for i in tempList:
            if int(i.packageID) == ID:
                print("Package ID: " + i.packageID + "\n" + "Address: " + i.packageAddress + "\n" +
                      "Deadline: " + i.deadline + "\n" + "City: " + i.city + "\n" + "Zipcode: " + i.zipCode +
                      "\n" + "Weight: " + i.mass + "\n" + "Status: " + i.status)

hashtable = HashTable()
hashtable.hashLookUp(13)

# import distance data
# how should distance data be stored?
# hubs should be knowledgeable of nearest hub that is still remaining to be delivered to

"""This section of code establishes the array that stores the WGUPS Distance data"""
width = 28
height = 28
arr = [[0 for i in range(width)] for j in range(height)]

class Hub:
    hubName = ""
    hubAddress = ""
    distToHubs = {}
    specificTruck = ""


"""This section of code imports the WGUPS Distance Data and stores it into the arr array variable"""
import csv
with open('WGUPS Distance Table.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in csvreader:                       # this for loop populates the data from the csv file into the arr variable
        for i in range(0, len(arr), 1):
            arr[count][i] = row[i]
        count = count + 1

# for each hub name , until hub name = hub name, traverse rows... then once the condition is satisfied (i.e., hub name == hub name, traverse column


def getKey(value, dictionary):
    keys = dictionary.keys()
    for i in keys:
        if dictionary[i] == value:
            return i

"""This section of code populates Hub objects with information such as the hub name and a dictionary of hubs with their distances stored as values"""
totalHubs = 27
hubList = []

for i in range(1, len(arr), 1):
    hubList.append(Hub())
    hubList[i-1].hubName = arr[i][0]  # gets name of hub in first column
    #destinationDict[hubList[i-1].hubName] = 0
    tempDict = {}
    for j in range(1, len(arr), 1):
        if i >= j:
            # sets dictionary key-value pair. Key = hub name, value = distance
            tempDict[arr[0][j]] = arr[i][j]

        if i < j:                # once i < j, iterations traverse a rows rather than columns
            tempDict[arr[j][0]] = arr[j][i]
    hubList[i-1].distToHubs = tempDict
    minimum = min(tempDict.values())
    del tempDict[getKey(minimum, tempDict)]

""" # Determines number of locations packages need to be delivered to and their addresses 
tempList1 = []
with open('WGUPS Package File.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")
    next(csvreader)  # skips over header row of CSV file
    for row in csvreader:
        if not(tempList1.__contains__(row[1])):
            tempList1.append(row[1])

print(len(tempList1)) """

# at this point, all hubs are aware of distances to other hubs relative to itself
# determine algorithm that (1) determines nearest neighbor... this must determine neaarest neighbor for truck1, then truck 2 (i.e., alternating)... truck 1 & truck 2 must pull
# from the same list
# check for deadlines
# check for special notes


#for row in arr:        # prints arr
    #print(row)

# the algorithm should determine which location is closest, but also compare priority based on deadlines. For example... x location is closest, but if i go to x, will I have time to get to the next location if needed?
# the algorithm should know where it currently is and what is the nearest destination to travel to.
# To determine if you have time to go to location x while still having time to go to location y afterward that has a specific time priority...
# create separate function that determines the distance between a given location to the location with the time restriction

# trucks need to have packages loaded onto them

# packages need to be tracked when they are dropped off

# each truck object needs to keep track of time

# route should be adaptive


# obj = HashTable()
# obj.hashLookUp(33)


# var = hashTable.__getitem__(0)[0]
# print(var.packageAddress)



def sortDistToHubs (currentHub):

    tempDict = {}
    for i in range(0, len(hubList), 1):
        if hubList[i].hubName == currentHub:
            tempDict = dict(sorted(hubList[i].distToHubs.items(), key=lambda item : float(item[1])))
            return tempDict


def packageAddressToHub (packageAddress):
    for i in range(0, len(hubList), 1):
        if hubList[i].hubName.__contains__(packageAddress):
            return hubList[i].hubName

def packagesReady (objList):
    temparr = []
    for obj in objList:
        if obj.status == "Ready for delivery":
            temparr.append(obj)
    return temparr


def getNearest(currentLocation, value):
    for hub in hubList:
        if hub.hubName == currentLocation:
            tempDict = sortDistToHubs(hub.hubName)
            items = list(tempDict.items())
            selecteditem = items[value]     # returns item set (e.g., ('Cottonwood Regional Softball Complex\n 4300 S 1300 E', '1.9')
            return selecteditem

def packagesByHub (hub):
    tempList = packagesReady(packageObjList)
    newArr = []
    for package in tempList:
        if hub.hubName.__contains__(package.packageAddress):
            newArr.append(package)
    return newArr

def getHubObjByName (hubName):
    for hub in hubList:
        if hub.hubName == hubName:
            return hub


truck1 = Truck()
truck1.name = "Truck 1"
truck2 = Truck()
truck2.name = "Truck 2"
numTrucks = 2
startingPointCount = 0
mainHub = hubList[0].hubName

"""Determines closest hub to current location that is provided"""
start = True
packages = packagesReady(packageObjList)
destinationList = []
destinationListCopy = []                            # intended to keep track of initial length of destination list
for obj in packages:
    hub = packageAddressToHub(obj.packageAddress)
    if not(destinationList.__contains__(hub)):
        destinationList.append(hub)
        destinationListCopy.append(hub)

print(destinationList)
print(len(destinationList))

for package in packageObjList:
    if package.specialNotes.__contains__("truck 2"):
        truck2.packageList.append(package)
        var = packageAddressToHub(package.packageAddress)
        truck2.destinations.append(var)
        destinationList.remove(var)
def loadPackages(currentHub, truck):
    i = 0
    found = False
    # compare currentAddress to address in destinationDict
    while (len(truck.destinations) < (len(destinationListCopy)/2)) and len(destinationList) != 0:
        while found == False:
            nearest = getNearest(currentHub, i)
            if destinationList.__contains__(nearest[0]) and nearest[0] != mainHub:
                found == True
                truck.destinations.append(nearest[0])
                packagesToLoad = packagesByHub(getHubObjByName(nearest[0]))
                for package in packagesToLoad:
                    truck.packageList.append(package)
                destinationList.remove(nearest[0])
                print("Call of load packages successful.Truck destinationList:", len(truck.destinations))
                loadPackages(nearest[0], truck)
            else:
                i += 1


    """if destinationDict.__contains__(currentHub):
        # if currentAddress is in destinationDict, get the distToHubs dictionary that corresponds witht the current address:
        for i in range (0, len(hubList), 1):
            if hubList[i].hubName.__contains__(currentHub): # once the corresponding distToHubs dictionary has been found, delete first min value (this has a distance value of zero)
                tempDict = hubList[j].distToHubs
                minimum = min(tempDict.values())
                del tempDict[getKey(minimum, tempDict)]
                minimum = min(tempDict.values())"""




    # if currentAddress is not in destinationDict






"""global found, startingPointCount
    found = False
    tempDict = {}
    for key in destinationList:
        if key == currentAddress:                # this for loop is to determine if the current address provides matches any of the addresses in the destination list
            for j in range(0, len(hubList), 1):                 # this for loop is to determine which hub corresponds with the destination/current address
                if hubList[j].hubName.__contains__(currentAddress):
                    tempDict = hubList[j].distToHubs
                    minimum = min(tempDict.values())
                    del tempDict[getKey(minimum, tempDict)] # deletes the hub with distance zero, as the hub with distance zero is the currrent location

                    while found == False:            # this code block determines if the selected nearest neighbor remains in the destination list (the other truck could have already visited)
                        minimum = min(tempDict.values())            # if the nearest neighbor was already visited, this determines the next closest location.
                        closestHub = getKey(minimum, tempDict)

                        if key



                        for key in destinationList:
                            print("k: ", k)
                            if closestHub.__contains__(key):         # determines if closestHub selected is still in the destination list

                                if destinationList


                                print(destinationList[k])
                                found = True
                                print(startingPointCount)
                                print(truck.name, " traveling from ", currentAddress, " to ", closestHub)
                                truck.packageList.append(closestHub)
                                if currentAddress == startingPoint and startingPointCount != numTrucks-1:
                                    startingPointCount = startingPointCount + 1
                                    print(startingPointCount)
                                    break
                                else:
                                    print("test2")
                                    del destinationList[destinationList.index(currentAddress)]     #deletes the address before

                            if k == (len(destinationList) - 1) and found == False:
                                del tempDict[getKey(minimum, tempDict)]
    if len(destinationList) == 0:
        print("complete")"""

# algorithm so far determines nearest address based on provided address
# should algorithm be run as is once to determine most efficient path for each truck simply to see which packages should be loaded onto which truck?
# a more advanced portion of the algorithm, when called a second time, will actually execute the truck route based on delivery deadlines and which packages need to be put on
# particular trucks?
x = 2
if x == 2:
    print("test")
elif x == 2:
    print("test2")
else:
    print("test3")

loadPackages(hubList[0].hubName, truck2)










