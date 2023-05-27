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
    speedMPH = 18
    time = datetime



#packageObjList = []  # list of all package objects

class HashTable:
    hashTable = {}  # blank hashtable (dictionary)
    for i in range(10):
        hashTable.__setitem__(i, [])

    #imports the WGUPS Package File
    import csv
    with open('WGUPS Package File.csv') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        next(csvreader)  # skips over header row of CSV file
        for row in csvreader:
            packageObj = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) # creates a package object
            bucket = int(packageObj.packageID) % 10     # determines which bucket to place the object in
            hashTable[bucket].append(packageObj)        # places the packageobj in the corresponding bucket

    def hashInsert(self, ID, address, deadline, city, zipcode, weight, status):
        packageObj = Package(ID, address, city, '', zipcode, deadline, weight, '')  # the first blank variable is the "state" variable, and the second blank variable is the "special instructions"
        packageObj.status = status
        bucket = int(packageObj.packageID) % 10  # determines which bucket to place the object in
        self.hashTable[bucket].append(packageObj)  # places the packageobj in the corresponding bucket

    def hashLookUp(self, ID):
        tempVar = ID % 10
        print(tempVar)
        tempList = self.hashTable.get(tempVar)
        print(tempList)
        for i in tempList:
            print(i.packageID)
            if int(i.packageID) == ID:
                print("test successful")





obj = HashTable()
obj.hashLookUp(33)






#var = hashTable.__getitem__(0)[0]
#print(var.packageAddress)