import datetime
import sys


# the Package class which stores information on each package processed by this program
class Package:
    def __init__(self, packageID, packageAddress, city, state, zipCode, deadline, mass, specialNotes):
        self.packageID = packageID
        self.packageAddress = packageAddress
        self.city = city
        self.state = state
        self.zipCode = zipCode
        self.deadline = deadline
        self.mass = mass
        self.specialNotes = specialNotes
        self.status = ""  # the status variable stores the package's current status (at the hub, en route, delayed, or delivered)
        self.readyTime = datetime  # the readyTime variable stores the package's time in which the package was first ready for delivery
        self.enrouteTime = datetime  # the enrouteTime variable stores the package's time in which the package was first en route to a destination
        self.delayedTime = datetime  # the delayedTime variable stores the package's time in which it was first deemed to be delayed, if at all
        self.deliveredTime = datetime  # the deliveredTime variable stores the package's time in which it was delivered to its destination


# the Truck class which stores information on trucks processed in this program
class Truck:
    def __init__(self):
        self.packageList = []
        self.destinations = []
        self.speedMPH = 18
        self.date_time = datetime.datetime(2000, 1, 1, 8, 0)
        self.name = ""
        self.milesTracker = 0
        self.currentLocation = ""

    # this function takes a datetime variable and adds it to the existing truck date_time variable.
    def setNewTime(self, timeChange):
        newDateTime = timeChange + self.date_time
        self.date_time = newDateTime


packageObjList = []  # list of all package objects taken from the WGUPS Package File.csv file
delayedPackages = []  # a list of all delayed packages


# this class is created to quickly and consistently change a package's status when appropriate
class StatusType:
    ready = "Ready for Delivery"
    enroute = "En Route"
    delivered = "Delivered"
    delayed = "Delayed"


# this class creates a hashtable for all package objects processed by this program for efficient searching abilities
class HashTable:
    hashTable = {}  # blank hashtable (dictionary)
    for i in range(10):
        hashTable.__setitem__(i, [])

    # imports the WGUPS Package File
    import csv
    with open('WGUPS Package File.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        next(csvreader)  # skips over header row of CSV file
        for row in csvreader:  # creates a package object based on the provided file. If the file has the term "Delay" in the spcial notes, then the package's status is marked as delayed.
            packageObj = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            if row[7].__contains__("Delay"):
                packageObj.status = StatusType.delayed
                packageObj.delayedTime = datetime.time(0,
                                                       0)  # the time in which the package is first known to be delayed is captured. It is assumed to be at 12AM (i.e., the start of the day)
                delayedPackages.append(packageObj)
            else:
                packageObj.status = StatusType.ready  # the default status for the package is 'Ready for Delivery'
                packageObj.readyTime = datetime.time(0,
                                                     0)  # the time in which the package is first known to be ready is captured. It is assumed to be at 12AM (i.e., the start of the day)

            packageObjList.append(packageObj)  # all objects are added to the packageObjList
            bucket = int(packageObj.packageID) % 10  # determines which bucket to place the object in
            hashTable[bucket].append(packageObj)  # places the packageobj in the corresponding bucket

    # this function adds a packageObj to the hashtable and to the packageObjList
    def hashInsert(self, ID, address, deadline, city, zipcode, weight, status):
        packageObj = Package(ID, address, city, '', zipcode, deadline, weight,
                             '')  # the first blank variable is the "state" variable, and the second blank variable is the "special instructions"
        packageObj.status = status
        bucket = int(packageObj.packageID) % 10  # determines which bucket to place the object in
        self.hashTable[bucket].append(packageObj)  # places the packageobj in the corresponding bucket

    # this function looks up information of a particular package by a user-provided integer ID
    def hashLookUp(self, ID):
        tempVar = ID % 10
        tempList = self.hashTable.get(tempVar)
        for i in tempList:
            if int(i.packageID) == ID:
                print("Package ID: " + i.packageID + "\n" + "Address: " + i.packageAddress + "\n" +
                      "Deadline: " + i.deadline + "\n" + "City: " + i.city + "\n" + "Zipcode: " + i.zipCode +
                      "\n" + "Weight: " + i.mass + "\n" + "Status: " + i.status)
                return i


hashtable = HashTable()  # instantiation of the HashTable class. Once instantiated, package information can become accessible to the user

# This section of code establishes the array that stores the WGUPS Distance data
width = 28
height = 28
arr = [[0 for i in range(width)] for j in
       range(height)]  # creates a 28 x 28 array of blank spaces (zeros act as placeholders)


# the Hub class which stores information on hubs processed in this program
class Hub:
    def __init__(self):
        hubName = ""
        hubAddress = ""
        distToHubs = {}
        specificTruck = ""


# This section of code imports the WGUPS Distance Data and stores it into the arr array variable
import csv

with open('WGUPS Distance Table.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in csvreader:  # this for loop populates the data from the csv file into the arr variable
        for i in range(0, len(arr), 1):
            arr[count][i] = row[i]
        count = count + 1


# this function returns a specific dictionary key based on user provided dictionary and value
def getKey(value, dictionary):
    keys = dictionary.keys()
    for i in keys:
        if dictionary[i] == value:
            return i


# This section of code populates Hub objects with information such as the hub name and a dictionary of hubs with their distances stored as values
totalHubs = 27
hubList = []  # a list of all hubs ultimatley read by the WGUPS Distance Table.csv file
for i in range(1, len(arr), 1):
    hubList.append(Hub())
    hubList[i - 1].hubName = arr[i][0]  # gets name of hub in first column
    tempDict = {}
    for j in range(1, len(arr), 1):
        if i >= j:
            # sets dictionary key-value pair. Key = hub name, value = distance
            tempDict[arr[0][j]] = arr[i][j]

        if i < j:  # once i < j, iterations traverse a rows rather than columns
            tempDict[arr[j][0]] = arr[j][i]
    hubList[i - 1].distToHubs = tempDict
    minimum = min(tempDict.values())
    del tempDict[getKey(minimum,
                        tempDict)]  # deletes the key value pair representing the distance to the same hub (zero miles). This information is not of any use.


# provided a given hub name, the hub's corresponding distToHubs variable (a dictionary containing distances to all other hubs; key = hub name, value = distance)
# is returned in an assorted manner from lowest value (shortest distance) to highest value (longest distance).
def sortDistToHubs(currentHub):
    tempDict = {}
    for i in range(0, len(hubList), 1):
        if hubList[i].hubName == currentHub:
            tempDict = dict(sorted(hubList[i].distToHubs.items(), key=lambda item: float(item[1])))
            return tempDict


# provided a given package address variable, the function returns the corresponding hub name that is associated with the package address
def packageAddressToHub(packageAddress):
    for i in range(0, len(hubList), 1):
        if hubList[i].hubName.__contains__(packageAddress):
            return hubList[i].hubName


# provided a variable that represents a list of objects, a list is returned which contains objects that have a status variable with a value that matches "Ready for Delivery"
def packagesReady(objList):
    temparr = []
    for obj in objList:
        if obj.status == StatusType.ready:
            temparr.append(obj)
    return temparr


# provided a variable that represents a list of objects, a list is returned which contains objects that have a status variable with a value that matches "En Route"
def packagesEnRoute(objList):
    temparr = []
    for obj in objList:
        if obj.status == StatusType.enroute:
            temparr.append(obj)
    return temparr


# provided an address (current location) and an integer value, a variable is returned with a single key and a single value. The single key-value pair is taken
# from the sortDistToHubs function, which returns a list of assorted key value pairs organized from lowest value to highest value. The integer value parameter for this
# function determines which index from the list returned by the sortDistToHubs function to return.
def getNearest(currentLocation, value):
    for hub in hubList:
        if hub.hubName == currentLocation:
            tempDict = sortDistToHubs(hub.hubName)
            items = list(tempDict.items())
            selecteditem = items[value]  # returns item set (e.g., ('Cottonwood Regional Softball Complex\n 4300 S 1300 E', '1.9')
            return selecteditem


# provided a hub object and a desired StatusType that is equal to "Ready for Delivery" or "En Route",
# this function will return a list of package objects in which the package address matches the name of the hub and the status type.
def packagesByHub(hub, statusType):
    tempList = []
    newArr = []
    if statusType == StatusType.ready:
        tempList = packagesReady(packageObjList)
    elif statusType == StatusType.enroute:
        tempList = packagesEnRoute(packageObjList)
    for package in tempList:
        if hub.hubName.__contains__(package.packageAddress):
            newArr.append(package)
    return newArr


# provided a hub name, this function returns the corresponding hub object that matches the provided name
def getHubObjByName(hubName):
    for hub in hubList:
        if hub.hubName == hubName:
            return hub


# instantiation of truck objects
truck1 = Truck()
truck1.name = "Truck 1"
truck2 = Truck()
truck2.name = "Truck 2"

mainHub = hubList[0].hubName  # a variable that holds the value of the WGU hub name

linkedPackageIDs = [1, 13, 14, 15, 16, 19, 29, 30]  # the variable that keeps track of all the packages that must be delivered together

packages = packagesReady(packageObjList)  # a list of packages that initially have a status of "Ready for Delivery"
destinationList = []  # a list of all destinations that both trucks shall travel to based on packages that have an initial status of "Ready for Delivery"
destinationListCopy = []  # intended to keep track of initial length of destination list
for obj in packages:  # this for loop adds destinations to the destinationList and destinationListCopy variables based on package adddress, and converting the packages address to a hub address
    hub = packageAddressToHub(obj.packageAddress)
    if not (destinationList.__contains__(hub)):
        destinationList.append(hub)
        destinationListCopy.append(hub)

for package in packages:  # this for loop adds destinations specifically to the truck 2 destinations variable (a list).
    if package.specialNotes.__contains__("truck 2"):
        hubAddress = packageAddressToHub(package.packageAddress)
        truck2.destinations.append(hubAddress)
        packagesToLoad = packagesByHub(getHubObjByName(hubAddress), StatusType.ready)
        for package in packagesToLoad:  # this for loop will add all packages with a status of "Ready for Delivery" if they are associated with
            truck2.packageList.append(package)  # a hub address in which a package is designated to go to and is required to be on truck 2
            package.status = StatusType.enroute  # changes the package status to "En Route"
            package.enrouteTime = datetime.time(8, 0)  # the time of the status change is 8 AM
        destinationList.remove(hubAddress)  # the hub address associated with the package is removed from the destinationList variable

    if linkedPackageIDs.__contains__(int(package.packageID)):  # this code block will add any package with a package ID listed in the linkedPackageIDs variable to truck 1's destinations variable
        hubAddress = packageAddressToHub(package.packageAddress)
        truck1.destinations.append(hubAddress)
        packagesToLoad = packagesByHub(getHubObjByName(hubAddress), StatusType.ready)
        for package in packagesToLoad:
            truck1.packageList.append(package)
            package.status = StatusType.enroute  # changes the status of the package to "En Route"
            package.enrouteTime = datetime.time(8, 0)  # the time of the status change is 8 AM
            if linkedPackageIDs.__contains__(int(package.packageID)):
                linkedPackageIDs.remove(int(package.packageID))  # the package ID is removed from the linkedPackageIDs list
        if destinationList.__contains__(hubAddress):
            destinationList.remove(hubAddress)  # the hub address associated with the package is removed from the destinationList

"""Truck 1 List prior to loadPackages function call:
Truck 1 13
Truck 1 39
Truck 1 14
Truck 1 15
Truck 1 16
Truck 1 34
Truck 1 19"""

"""Truck 2 List prior to loadPackages function call:
Truck 2 3
Truck 2 18
Truck 2 36
Truck 2 5
Truck 2 37
Truck 2 38"""

"""destinationListCopy length: 24"""
print("destinationListCopy length: ", len(destinationListCopy))
print("destinationList length: ", len(destinationList))


def loadPackages(currentHub, truck):
    i = 0
    found = False
    while found == False:
        if i <= len(hubList)-1:  # this checks to see if the i integer value is <= the total length of the destinationListCopy variable
            nearest = getNearest(currentHub, i)  # this returns the nearest hub relative to the hub parameter entered (nearest[0]) and the distance from the currentHub variable (nearest[1])
            if destinationList.__contains__(nearest[0]) and nearest[0] != mainHub:
                found = True
                packagesToLoad = packagesByHub(getHubObjByName(nearest[0]),
                                               StatusType.ready)  # the packagesToLoad parameter stores the packages that are going to be delivered to the hub stored within the "nearest" variable
                if len(packagesToLoad) + len(
                        truck.packageList) > 16:  # trucks can't store more than 16 packages at a time. Nothing is done with the "packagesToLoad variable" if this logic test is true.
                    found = True
                else:
                    truck.destinations.append(nearest[0])  # if the above logic test is false... the destination of the nearest hub is added to the truck's destinations variable
                    for package in packagesToLoad:  # the packages in the packagesToLoad variable are added to the truck packageList variable,
                        truck.packageList.append(package)  # the package status is change to "En Route", and
                        package.status = StatusType.enroute  # the time that the package status is changed to "En Route" (8AM) is captured
                        package.enrouteTime = datetime.time(8, 0)
                    destinationList.remove(nearest[0])  # the hub name is removed from the destinationList variable
                    print(truck.name, "length of len(truck.destinations)", len(truck.destinations),
                          "Truck packageList size: ", len(truck.packageList), "\n")
                    loadPackages(nearest[0],
                                 truck)  # the function is recursively called for the hub name represented as nearest[0]
            else:  # if the hub name represented by the nearest[0] value is not within the destinationList, the next closest hub & distance is obtained in the call to getNearest()
                i += 1
        else:
            found = True


arrivalTime = datetime.datetime(2000, 1, 1, 9, 5)
changeStatus = False
truck2TravelBack = False
truck1TravelBack = False


# write code that delivers packages, tracks the time, and checks that package deadlines can be met
def deliverClosestPackages(currentHub, truck):
    global truck2TravelBack, truck1TravelBack, changeStatus
    i = 0
    found = False
    while found == False:
        if i <= len(hubList)-1:
            nearest = getNearest(currentHub, i)                                             # gets the nearest hub based on currentHub parameter
            if truck.destinations.__contains__(nearest[0]):                                 # if the nearest hub is within the truck.destination's variable...
                found = True

                elapsedTimeMinutes = float(nearest[1]) * (1 / truck.speedMPH) * 60          # this code block establishes the new time for the truck since it has left the main WGU hub
                newTime = datetime.timedelta(minutes=elapsedTimeMinutes)
                truck.setNewTime(newTime)

                truck.currentLocation = nearest[0]                                          # this code block tracks the truck's location and the amount of miles travelled
                truck.milesTracker += float(nearest[1])

                packagesToUnload = packagesByHub(getHubObjByName(nearest[0]), StatusType.enroute)
                for package in packagesToUnload:
                    if truck.packageList.__contains__(package):                             # if the truck's package list contains the packages that are associated with the hub and the "En Route" status...
                        package.status = StatusType.delivered
                        package.deliveredTime = truck.date_time.time()
                        print("unloaded package: ", package.packageID)
                truck.destinations.remove(nearest[0])                                       # the closest hub (nearest[0]) is removed from the truck destinations variable
                print("\n", truck.name, truck.milesTracker, truck.currentLocation, truck.date_time)

                if truck.date_time > arrivalTime and changeStatus == False:                 # once one (1) truck date_time variable is greater than the arrivalTime variable (the time in which initially delayed packages are marked as "at the hub"),
                    changeStatus = True                                                     # the status of the packages that were initially delayed are changed to "at the hub"
                    for package in delayedPackages:
                        package.status = StatusType.ready
                        package.readyTime = arrivalTime.time()

                if truck.name == "Truck 2" and truck.date_time > arrivalTime and truck2TravelBack == False:     # this if statement returns true once and is intended to control truck 2 travelling back to the WGU hub to pick up additional packages
                    truck2TravelBack = True                                             # this variable allows this if statement to only fire once
                    hub = getHubObjByName(truck.currentLocation)
                    distanceToMainHub = float(hub.distToHubs[mainHub])
                    print("travelling to mainHub")
                    truck.milesTracker += distanceToMainHub
                    print(truck.name, truck.milesTracker)
                    elapsedTimeMinutes = distanceToMainHub * (1 / truck.speedMPH) * 60
                    newTime = datetime.timedelta(minutes=elapsedTimeMinutes)
                    truck.setNewTime(newTime)
                    print("arrived at mainHub")
                    for package in packageObjList:                                                      # this for loop will pick out all packages that have a remaining status of "at the hub" and have a specific deadline (i.e., not "EOD")
                        if package.status == StatusType.ready and package.deadline != "EOD":
                            print(package.packageID)
                            truck.packageList.append(package)                                           # packages are amended to the truck's packageList variable
                            if not (truck.destinations.__contains__(packageAddressToHub(package.packageAddress))):  # if the truck destinations list does not already contain the hub address to be appended...append the hub address
                                truck.destinations.append(packageAddressToHub(package.packageAddress))
                            package.status = StatusType.enroute                                         # mark the package status as "En Route"
                            package.enrouteTime = truck.date_time.time()                                # capture the time in which the package status was changed to "En Route"
                    deliverClosestPackages(mainHub, truck)                                              # continue the call to deliverClosestPackages

                if truck.name == "Truck 1" and len(truck.destinations) == 0 and truck1TravelBack == False:  # once truck 1 has delivered all of the packages that were initially loaded, truck one heads back to the WGU hub
                    truck1TravelBack = True                                         # this variable allows this if statement to only fire once
                    hub = getHubObjByName(truck1.currentLocation)
                    distanceToMainHub = float(hub.distToHubs[mainHub])
                    print("truck 1 travelling to mainHub")
                    truck.milesTracker += distanceToMainHub
                    elapsedTimeMinutes = distanceToMainHub * (1 / truck.speedMPH) * 60
                    newTime = datetime.timedelta(minutes=elapsedTimeMinutes)
                    truck.setNewTime(newTime)
                    print("truck 1 arrived at mainHub")
                    for package in packageObjList:                                                          # this for loop will pick out all packages that have a remaining status of "at the hub" and have do not have a specific deadline (i.e., "EOD")
                        if package.status == StatusType.ready and package.deadline == "EOD":
                            print(package.packageID)
                            truck.packageList.append(package)                                               # packages are amended to the truck's packageList variable
                            if not (truck.destinations.__contains__(packageAddressToHub(package.packageAddress))): # if the truck destinations list does not already contain the hub address to be appended...append the hub address
                                truck.destinations.append(packageAddressToHub(package.packageAddress))
                            package.status = StatusType.enroute                                             # mark the package status as "En Route"
                            package.enrouteTime = truck.date_time.time()                                    # capture the time in which the package status was changed to "En Route"
                    deliverClosestPackages(mainHub, truck)                                                  # continue the call to deliverClosestPackages

                if len(truck.destinations) != 0:
                    deliverClosestPackages(nearest[0], truck)
            else:
                i += 1
        else:
            found = True

timeOfCorrectedMistake = datetime.datetime(2000, 1, 1, 10, 20)

def correctPackageMistake(packageID, correctedPackageLoc):
    packageToCorrect = hashtable.hashLookUp(packageID)
    packageToCorrect.status = StatusType.ready

    currentPackageLoc = packageToCorrect.packageAddress

    currentTruckLoc = truck2.currentLocation
    hub = getHubObjByName(currentTruckLoc)

    distance = float(hub.distToHubs[packageAddressToHub(currentPackageLoc)])
    truck2.milesTracker += distance
    elapsedTimeMin = distance * (1 / truck1.speedMPH) * 60
    newTime = datetime.timedelta(minutes=elapsedTimeMin)
    truck2.setNewTime(newTime)
    truck2.packageList.append(packageToCorrect)
    truck2.destinations.append(packageAddressToHub(correctedPackageLoc))
    truck2.currentLocation = packageAddressToHub(currentPackageLoc)
    print("length of destinations", len(truck2.destinations), "miles: ", distance)
    packageToCorrect.status = StatusType.enroute
    print("travelled to hub where package was delivered")

    deliverClosestPackages(truck2.currentLocation, truck2)

    """# Code for travelling to corrected location
    currentTruckLoc = packageAddressToHub(currentPackageLoc)
    truck1.currentLocation = currentTruckLoc
    hub = getHubObjByName(currentTruckLoc)
    distance = float(hub.distToHubs[packageAddressToHub(correctedPackageLoc)])
    truck1.milesTracker += distance
    elapsedTimeMin = distance * (1 / truck1.speedMPH) * 60
    newTime = datetime.timedelta(minutes=elapsedTimeMin)
    truck1.setNewTime(newTime)
    packageToCorrect.status = StatusType.delivered
    print("Delivered to corrected location")"""


# Load packages initially onto 2 trucks based on packages available for delivery
loadPackages(hubList[0].hubName, truck2)
loadPackages(hubList[0].hubName, truck1)
for package in truck1.packageList:
    print(truck1.name, package.packageID)

for package in truck2.packageList:
    print(truck2.name, package.packageID)

deliverClosestPackages(hubList[0].hubName, truck1)
deliverClosestPackages(hubList[0].hubName, truck2)
correctPackageMistake(9, "410 S State St")



"------------------------------TESTING----------------------------------------"

print("Welcome to the program")

#if sys.argv[1] == "Get":
    #print("test successful")

# for destination in truck2.destinations:
# t2.append(destination)

# for destination in truck1.destinations:
# t1.append(destination)
print(truck1.milesTracker + truck2.milesTracker)

"""

Please enter from the following options:

Input: 1
Output: An option for the user to enter the package ID (1-40) and a specific time. The output will tell them the status of the package at the desired time

Input: 2
Output: Snapshots of all packages at X time (see requirements)

Input: 3
Output: Snapshots of all packages at Y time (see requirements)

Input: 4
Output: Snapshots of all packages at Z time (see requirements)



Pseudocode:

when package objects are created: package.readyTime = datetime.time(0, 0)

when package objects are loaded onto trucks: package.associatedTruck = truck.name
                                             package.enrouteTime = date.time(truck.date_time.time())

when package objects are unloaded:          package.delivered = date.time(truck.date_time.time())

Input 1:

packageInQuestions = hashTable.hashsearch(providedID)
providedTimeByUser = X

if providedTimeByUser >= packageInQuestions.readyTime and less than packageInQuestions.enroutetime
    ready

... repeat similar if statements for other options


"""









