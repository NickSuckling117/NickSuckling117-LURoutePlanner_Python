#This section imports the external libaries this module needs
import sqlite3 as sql
import time
import hashlib

#This section defines what database needs to be opened and then opens it and creates a cursor
path = "LondonUndergroundDB.db"
db = sql.connect(path)
c = db.cursor()

print("Loaded SQLHandler")

#This subroutine closes the database
def QuitPressed():
    db.close()

#This subroutine takes details the user entered in the GUI to create a new user and hashes the password using md5 before adding it to the database
def CreateNewUser(username, password, firstname, surname):
    encodedPassword = hashlib.md5(password.encode())
    hashedPassword = encodedPassword.hexdigest()
    existingUser = False
    usernames = c.execute("""
SELECT Username
FROM tblUsers""")
#This section of code is used to find if there is a user with the same username that already exists in the database.
    for i in usernames:
        if i[0][:] == username:
            existingUser = True
            print("user already exists")
            break
    if existingUser == False:
            print("adding user")
            c.execute("""INSERT INTO tblUsers(Username, Password, Firstname, Surname)
VALUES('{0}', '{1}', '{2}', '{3}')""".format(username, hashedPassword, firstname, surname))
            db.commit()
    return existingUser

#This subroutine takes details entered by the user on the login screen and compares those details to those in the database
def ValidateUser(username, password):
    valid = False
    encodedPassword = hashlib.md5(password.encode())
    hashedPassword = encodedPassword.hexdigest()
    c.execute("""
SELECT Username
FROM tblUsers""")
    usernames = list(c.fetchall())
    for i in usernames:
        if i[0][:] == username:
            valid = True
            break
        else:
            valid = False

#this section of code only runs if a matching username has been found
    if valid == True:
        c.execute("""
SELECT Password
FROM tblUsers
WHERE Username = '{0}'""".format(username))
        correctPassword = c.fetchone()

        if correctPassword[0][:] == hashedPassword:
            valid = True
        else:
            valid = False
    return valid

#This subroutine gets the users first name based on their username
def GetCurrentFirstname(username):
    c.execute("""
SELECT Firstname
FROM tblUsers
WHERE Username = '{0}'""".format(username))
    userFirstname = c.fetchone()
    return userFirstname

#This subroutine gets the users surname based on their username
def GetCurrentSurname(username):
    c.execute("""
SELECT Surname
FROM tblUsers
WHERE Username = '{0}'""".format(username))
    userSurname = c.fetchone()
    return userSurname

#This suroutine uses the previous two subroutines to get the full name of the user
def GetCurrentFullname(username):
    currentFirstname = GetCurrentFirstname(username)
    currentSurname = GetCurrentSurname(username)
    currentFullname = currentFirstname[0][:] + " " + currentSurname[0][:]
    return currentFullname

#This subroutine gets the open/closed status of every station in the database
def GetAllStationsStatus():
    stationStatusDict = {}
    c.execute("""SELECT StationName, OpenClosed
FROM tblStations
ORDER BY StationName""")
    stationStatus = c.fetchall()
    for i in stationStatus:
        stationStatusDict[str(i[0][:])] = i[1]
    return stationStatusDict

#This subroutine get the open/closed value of a single station that the program specifies using its name
def GetStationStatus(stationName):
    c.execute("""SELECT OpenClosed
FROM tblStations
WHERE StationName = '{0}'""".format(stationName))
    temp = c.fetchone()
    return temp[0]

#This subroutine get the open/closed value of a single station that the program specifies using its ID
def GetStationStatusFromID(stationID):
    c.execute("""SELECT OpenClosed
FROM tblStations
WHERE StationID = '{0}'""".format(stationID))
    temp = c.fetchone()
    return temp[0]

#This subroutine retrieves all of the station IDs in the SQL database
def GetAllStationIDs():
    c.execute("""SELECT StationID FROM tblStations""")
    tempStationIDs = list(c.fetchall())
    stationIDs = []
    for i in tempStationIDs:
        stationIDs.append(i[0][:])
    return stationIDs

#This subroutine gets the stations name based on its ID
def GetStationName(ID):
    c.execute("""SELECT StationName
FROM tblStations
WHERE StationID = '{0}'""".format(ID))
    temp = c.fetchone()
    return temp[0]

#This subroutine takes the station ID and the new station status from the open close screen and updates it to the new value in the SQL database
def UpdateOpenCloseValue(ID, status):
    c.execute("""UPDATE tblStations
SET OpenClosed = '{0}'
WHERE StationID = '{1}'""".format(status, ID))
    db.commit()

#This subroutine retrieves all of the names of the stations with a status of 1 (OPEN)
def GetAllOpenStationNames():
    c.execute("""SELECT StationName
FROM tblStations
WHERE OpenClosed = 1
ORDER BY StationName """)
    allOpenStationNamesTemp = c.fetchall()
    allOpenStationNames = []
    for i in allOpenStationNamesTemp:
        allOpenStationNames.append(i[0][:])
    return allOpenStationNames

#This gets the name of the current node being looked at in dijkstra's algorithm
def GetCurrentNodeName(StationID):
    c.execute("""SELECT StationName
FROM tblStations
WHERE StationID = '{0}'""".format(StationID))
    temp = c.fetchone()
    stationName = temp[0][:]
    return stationName

#This subroutine gets the IDs of all of the stations adjacent to the current node
def GetCurrentNodeAdjacentConnections(StationID):
    allConnections = []
    connections = []
    c.execute("""SELECT N,E,S,W,X
FROM tblConnections
WHERE StationID = '{0}'""".format(StationID))
    temp = c.fetchall()
    for record in temp:
        for field in record:
            connections.append(field)
        allConnections.append(connections)
        connections = []
    return allConnections

#This subroutine retrieves the line IDs of all of the stations on a specific node
def GetLinesOnCurrentNode(StationID):
    '''This functions gets the lines on the current node'''
    lines = []
    c.execute("""SELECT LineID
FROM tblConnections
WHERE StationID = '{0}'""".format(StationID))
    temp = c.fetchall()
    for i in temp:
        lines.append(i[0][:])
    return lines

#This subroutine retrieves the station and its distance from the current station to the north of the current node on a single line
def GetAdjacentNorthStationToCurrentNode(LineID, StationID):
    northConnection = []
    c.execute("""SELECT N, NDistance
FROM tblConnections
WHERE LineID = '{0}' AND StationID = '{1}'""".format(LineID, StationID))
    temp = c.fetchall()
    for i in temp:
        northConnection.append(i[0][:])
        northConnection.append(i[1])
    return northConnection

#This subroutine retrieves the station and its distance from the current station to the east of the current node on a single line
def GetAdjacentEastStationToCurrentNode(LineID, StationID):
    eastConnection = []
    c.execute("""SELECT E, EDistance
FROM tblConnections
WHERE LineID = '{0}' AND StationID = '{1}'""".format(LineID, StationID))
    temp = c.fetchall()
    for i in temp:
        eastConnection.append(i[0][:])
        eastConnection.append(i[1])
    return eastConnection

#This subroutine retrieves the station and its distance from the current station to the south of the current node on a single line
def GetAdjacentSouthStationToCurrentNode(LineID, StationID):
    southConnection = []
    c.execute("""SELECT S, SDistance
FROM tblConnections
WHERE LineID = '{0}' AND StationID = '{1}'""".format(LineID, StationID))
    temp = c.fetchall()
    for i in temp:
        southConnection.append(i[0][:])
        southConnection.append(i[1])
    return southConnection

#This subroutine retrieves the station and its distance from the current station to the west of the current node on a single line
def GetAdjacentWestStationToCurrentNode(LineID, StationID):
    westConnection = []
    c.execute("""SELECT W, WDistance
FROM tblConnections
WHERE LineID = '{0}' AND StationID = '{1}'""".format(LineID, StationID))
    temp = c.fetchall()
    for i in temp:
        westConnection.append(i[0][:])
        westConnection.append(i[1])
    return westConnection

#This subroutine retrieves the station and its distance from the current station. (Extra connection used if a station has more than 4 connection on a line)
def GetAdjacentExtraStationToCurrentNode(LineID, StationID):
    extraConnection = []
    c.execute("""SELECT X, XDistance
FROM tblConnections
WHERE LineID = '{0}' AND StationID = '{1}'""".format(LineID, StationID))
    temp = c.fetchall()
    for i in temp:
        extraConnection.append(i[0][:])
        extraConnection.append(i[1])
    return extraConnection

#This subroutine runs all of the get adjacent station subroutines for each line the node is on and then applies those to the current node
def GetStationsAdjacentToCurrentNode(StationID):
    adjacent = {}
    stations = {}
    tempLines = GetLinesOnCurrentNode(StationID)
    for ID in tempLines:
        adjacent[ID] = None
    for LineID in adjacent:
        northConnection = GetAdjacentNorthStationToCurrentNode(LineID, StationID)
        if northConnection[0] == "0":
            pass
        else:
            stations[northConnection[0]] = northConnection[1]
        eastConnection = GetAdjacentEastStationToCurrentNode(LineID, StationID)
        if eastConnection[0] == "0":
            pass
        else:
            stations[eastConnection[0]] = eastConnection[1]
        southConnection = GetAdjacentSouthStationToCurrentNode(LineID, StationID)
        if southConnection[0] == "0":
            pass
        else:
            stations[southConnection[0]] = southConnection[1]
        westConnection = GetAdjacentWestStationToCurrentNode(LineID, StationID)
        if westConnection[0] == "0":
            pass
        else:
            stations[westConnection[0]] = westConnection[1]
        extraConnection = GetAdjacentExtraStationToCurrentNode(LineID, StationID)
        if extraConnection[0] == "0":
            pass
        else:
            stations[extraConnection[0]] = extraConnection[1]
        adjacent[LineID] = stations
        stations = {}
    return adjacent

#This subroutine gets the open/closed status value for the current station being looked at in the dijkstra's algorithm
def GetOpenClosedValueForCurrentNode(StationID):
    openValue = False
    c.execute("""SELECT OpenClosed
FROM tblStations
WHERE StationID = '{0}'""".format(StationID))
    temp = c.fetchone()
    if temp[0] == 0:
        openValue = False
    else:
        openValue = True
    return openValue

#This subroutine gets the stations ID from the stations name
def GetStationIDFromStationName(StationName):
    c.execute("""SELECT StationID
FROM tblStations
WHERE StationName = '{0}'""".format(StationName))
    temp = c.fetchone()
    ID = temp[0]
    return ID

#This subroutine gets the stations name from the stations ID
def GetStationNameFromStationID(StationID):
    c.execute("""SELECT StationName
FROM tblStations
WHERE StationID = '{0}'""".format(StationID))
    temp = c.fetchone()
    name = temp[0]
    return name

#This gets the line ID from the line name
def GetLineIDFromLineName(LineName):
    c.execute("""SELECT LineID
FROM tblLines
WHERE LineName = '{0}'""".format(LineName))
    temp = c.fetchone()
    ID = temp[0]
    return ID

#This subroutine gets the line name from the line ID
def GetLineNameFromLineID(LineID):
    c.execute("""SELECT LineName
FROM tblLines
WHERE LineID = '{0}'""".format(LineID))
    temp = c.fetchone()
    name = temp[0]
    return name

#This algorithm takes the user's selected start and end station names and uses them to see if a route already exists in the database.
def CheckIfRouteExists(start, end):
    startID = GetStationIDFromStationName(start)
    endID = GetStationIDFromStationName(end)
    c.execute("""SELECT RouteID
FROM tblRoutes
WHERE StartID = '{0}' AND EndID = '{1}'""".format(startID, endID))
    temp = c.fetchone()
    if temp == None:
        routeExists = False
    else:
        routeExists = temp[0]
        print("Route found between {0} and {1}".format(start, end))
    return routeExists

#This subroutine retrieves all of the instructions needed to display a route to the user if the route has already been calculated
def GetExistingRoute(routeID):
    c.execute("""SELECT Station1, Station2, Line, Distance
FROM tblRouteParts
WHERE RouteID = {0}
ORDER BY Ord """.format(routeID))
    temp = c.fetchall()
    fullRoute = []
    for i in temp:
        station1Name = GetStationNameFromStationID(i[0])
        station2Name = GetStationNameFromStationID(i[1])
        lineName = GetLineNameFromLineID(i[2])
        fullRouteSegment = []
        fullRouteSegment.append(station1Name)
        fullRouteSegment.append(station2Name)
        fullRouteSegment.append(lineName)
        fullRouteSegment.append(i[3])
        print(fullRouteSegment)
        fullRoute.append(fullRouteSegment)
    return fullRoute

#This subroutine adds a new route and its instructions to the database once it has been generated
def addNewRoute(start, end, routeDetails):
    c.execute("""INSERT INTO tblRoutes (StartID, EndID)
VALUES ('{0}' ,'{1}')""".format(start, end))

    c.execute("""SELECT RouteID FROM tblRoutes WHERE RouteID = (SELECT MAX(RouteID) FROM tblRoutes)""")
    routeID = c.fetchone()
    orderCounter = 1
    for segment in routeDetails:
        station1ID = GetStationIDFromStationName(segment[0])
        station2ID = GetStationIDFromStationName(segment[1])
        LineID = GetLineIDFromLineName(segment[2])
        c.execute("""INSERT INTO tblRouteParts (Station1, Station2, Line, Distance, RouteID, Ord)
VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(station1ID, station2ID, LineID, segment[3], routeID[0], orderCounter))
        orderCounter += 1
        
    db.commit()

#This subroutine adds a route to that users favourites if the user selects to do so.
def AddRouteToFavourites(startName, endName, username):
    name = startName + " to " + endName
    c.execute("""SELECT FavouriteID FROM tblFavourites
WHERE Username = '{0}' AND Name = '{1}'""".format(username, name))
    exists = c.fetchone()
    if exists == None:
        startID = GetStationIDFromStationName(startName)
        endID = GetStationIDFromStationName(endName)
        c.execute("""INSERT INTO tblfavourites (Username, StartID, EndID, Name)
VALUES ('{0}', '{1}', '{2}', '{3}')""".format(username, startID, endID, name))
        db.commit()

    return exists

#This subroutine gets all of the name of the favourite routes for the current user
def GetAllFavouriteRouteNames(username):
    c.execute("""SELECT Name from tblFavourites
WHERE Username = '{0}'""".format(username))
    names = []
    temp = c.fetchall()
    for i in temp:
        names.append(i[0][:])
    return names
