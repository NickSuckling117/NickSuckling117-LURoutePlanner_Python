#This section of code is used to import all of the necessary modules and libraies
#needed for the program to run.
import tkinter as tk
from tkinter import ttk
import SQLHandler as sql
import Graph as graph
import pydocx as pd
PILImportSuccess = False
try:
    from PIL import Image, ImageTk
    PILImportSuccess = True
except ImportError:
    print("Unable to import PIL")

#This section of code creates the GUI class. It creates some attributes that will be needed later on and also runs the methods
#needed to create all of the necessary frames.
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.width, self.height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.config(width = self.width, height = self.height)
        self.root.state("zoomed")
        self.root.title("London Underground Navigation Assistant")
        self.mainFrame = tk.Frame(self.root, height = self.height, width = self.width, bg = "Black")
        self.mainFrame.grid(row = 0, column = 0)
        self.currentSelectionFrame = 0
        self.mapOpen = 0
        self.frames = {}
        self.currentUsername = None
        self.CreateLogin()
        self.CreateUser()
        self.CreateMainMenu()
        self.CreateOpenClose()
        self.CreateRoutePlanner()
        self.CreateFavourites()
        self.CreateStationSelect()
        self.CreateRouteInstructions()
        self.RaiseLogin()

#This subroutine creates the login screen
    def CreateLogin(self):        
        self.loginFrame = tk.Frame(self.mainFrame, width = self.width, height = self.height, bg = "Yellow")
        self.loginFrame.grid(row = 0, column = 0)
        self.loginFrame.grid_propagate(False)

        self.loginUsernameLabel = tk.Label(self.loginFrame, bg = "Yellow", text = "Username")
        self.loginUsernameLabel.grid(row = 0, column = 0)
        self.loginPasswordLabel = tk.Label(self.loginFrame, bg = "Yellow", text = "Password")
        self.loginPasswordLabel.grid(row = 1, column = 0)
        self.loginUsernameEntry = tk.Entry(self.loginFrame)
        self.loginUsernameEntry.grid(row = 0, column = 1)
        self.loginPasswordEntry = tk.Entry(self.loginFrame, font = "Webdings 7", show = "=")
        self.loginPasswordEntry.grid(row = 1, column = 1)
        self.loginValidationLabel = tk.Label(self.loginFrame, bg = "Yellow")
        self.loginValidationLabel.grid(row = 2, column = 0, columnspan = 2)
        self.loginConfirmButton = tk.Button(self.loginFrame, text = "Login", command = self.ValidateUser)
        self.loginConfirmButton.grid(row = 3, column = 0)
        self.loginAddNewUserButton = tk.Button(self.loginFrame, text = "Add New User", command = self.RaiseUser)
        self.loginAddNewUserButton.grid(row = 3, column = 1)
        self.quitButton = tk.Button(self.loginFrame, text = "Quit", command = self.QuitPressed)
        self.quitButton.grid(row = 3, column = 2)

        self.frames["LoginFrame"] = self.loginFrame

#This subroutine raises the login screen
    def RaiseLogin(self):
        self.currentUsername = None
        self.ResetLogin()
        self.frames["LoginFrame"].tkraise()

#This subroutine resests the login screen
    def ResetLogin(self):
        self.loginFrame.destroy()
        self.CreateLogin()

#This subroutine gets the values the user entered on the login screen
#so they can be passed onto another subroutine that confirms their
#login details.
    def ValidateUser(self):
        currentUsername = str(self.loginUsernameEntry.get())
        currentPassword = str(self.loginPasswordEntry.get())
        valid = sql.ValidateUser(currentUsername, currentPassword)
#this if statement raises the login screen
        if valid == True:
            self.currentUsername = currentUsername
            self.RaiseMainMenu()
            self.loginValidationLabel.config(text = "")
#This displays a message to the user that their details were incorrect
        else:
            self.loginValidationLabel.config(text = "Incorrect Username or Password")

#This subroutibe causes the program to close
    def QuitPressed(self):
        sql.QuitPressed()
        quit()

#This subroutine creates the create user screen
    def CreateUser(self):
        self.userFrame = tk.Frame(self.mainFrame, width = self.width, height = self.height, bg = "Red")
        self.userFrame.grid(row = 0, column = 0)
        self.userFrame.grid_propagate(False)

        self.userUsernameLabel = tk.Label(self.userFrame, bg = "Red", text = "Enter Username")
        self.userUsernameLabel.grid(row = 0, column = 0)
        self.userFirstnameLabel = tk.Label(self.userFrame, bg = "Red", text = "Enter Firstname")
        self.userFirstnameLabel.grid(row = 1, column = 0)
        self.userSurnameLabel = tk.Label(self.userFrame, bg = "Red", text = "Enter Surname")
        self.userSurnameLabel.grid(row = 2, column = 0)
        self.userNewPasswordLabel = tk.Label(self.userFrame, bg = "Red", text = "Enter password")
        self.userNewPasswordLabel.grid(row = 3, column = 0)
        self.userConfirmNewPasswordLabel = tk.Label(self.userFrame, bg = "red", text = "Confirm New Password")
        self.userConfirmNewPasswordLabel.grid(row = 4, column = 0)
        self.userUsernameEntry = tk.Entry(self.userFrame)
        self.userUsernameEntry.grid(row = 0, column = 1)
        self.userFirstnameEntry = tk.Entry(self.userFrame)
        self.userFirstnameEntry.grid(row = 1, column = 1)
        self.userSurnameEntry = tk.Entry(self.userFrame)
        self.userSurnameEntry.grid(row = 2, column = 1)
        self.userNewPasswordEntry = tk.Entry(self.userFrame, font = "Webdings 7", show = "=")
        self.userNewPasswordEntry.grid(row = 3, column = 1)
        self.userConfirmNewPasswordEntry = tk.Entry(self.userFrame, font = "Webdings 7", show = "=")
        self.userConfirmNewPasswordEntry.grid(row = 4, column = 1)
        self.userCreateNewUserButton = tk.Button(self.userFrame, text = "Add New User", command = self.AddNewUser)
        self.userCreateNewUserButton.grid(row = 5, column = 0)
        self.userStatusLabel = tk.Label(self.userFrame, bg = "Red")
        self.userStatusLabel.grid(row = 6, column = 0, columnspan = 2)
        self.userBack = tk.Button(self.userFrame, text = "Back", command = self.RaiseLogin)
        self.userBack.grid(row = 7, column = 0)

        self.frames["CreateNewUserFrame"] = self.userFrame

#This subroutine raises the create user frame
    def RaiseUser(self):
        self.frames["CreateNewUserFrame"].tkraise()

#This subroutine gets all of the users entered details and checks if they are valid
    def AddNewUser(self):
        newUsername = str(self.userUsernameEntry.get())
        newFirstname = str(self.userFirstnameEntry.get())
        newSurname = str(self.userSurnameEntry.get())
        newPassword = str(self.userNewPasswordEntry.get())
        confirmPassword = str(self.userConfirmNewPasswordEntry.get())

        if len(newUsername) <1:
            self.userStatusLabel.config(text = "No username entered")

        elif len(newFirstname) <1:
            self.userStatusLabel.config(text = "First name not entered")

        elif len(newSurname) <1:
            self.userStatusLabel.config(text = "Surname not entered")

        elif len(newPassword) <1:
            self.userStatusLabel.config(text = "No password entered")
        
        elif confirmPassword != newPassword:
            self.userStatusLabel.config(text = "Passwords do not match")

        else:
            existingUser = sql.CreateNewUser(newUsername, newPassword, newFirstname, newSurname)
            if existingUser == True:
                self.userStatusLabel.config(text = "Username already exists")
            else:
                self.userStatusLabel.config(text = "User Created")

#This subroutine creates the main menu.
    def CreateMainMenu(self):
        self.mainMenuFrame = tk.Frame(self.mainFrame, bg = "Grey", width = self.width, height = self.height)
        self.mainMenuFrame.grid(row = 0, column = 0)
        self.mainMenuFrame.grid_propagate(False)

        self.mainDisplayNameLabel = tk.Label(self.mainMenuFrame, bg = "Grey")
        self.mainDisplayNameLabel.grid(row = 0, column = 0)
        self.mainRoutePlannerButton = tk.Button(self.mainMenuFrame, text = "Route Planner", command = self.RaiseRoutePlanner)
        self.mainRoutePlannerButton.grid(row = 1, column = 0)
        self.mainOpenClosedStationsButton = tk.Button(self.mainMenuFrame, text = "Open/Closed Stations", command = self.RaiseOpenClose)
        self.mainOpenClosedStationsButton.grid(row = 1, column = 1)
        if PILImportSuccess == True:
            self.mainMapButton = tk.Button(self.mainMenuFrame, text = "Map", command = self.OpenMapFile)
            self.mainMapButton.grid(row = 1, column = 2)
        self.mainLogoutButton = tk.Button(self.mainMenuFrame, text = "Logout", command = self.RaiseLogin)
        self.mainLogoutButton.grid(row = 2, column = 0)


        self.frames["MainMenuFrame"] = self.mainMenuFrame

#This subroutine raises the main menu
    def RaiseMainMenu(self):
        self.mainDisplayNameLabel.config(text = "Welcome Back {0}".format(self.GetUserNames()))
        self.frames["MainMenuFrame"].tkraise()

#This subroutine gets the current users username so it can be used to get their full name
    def GetUserNames(self):
        currentUsername = str(self.loginUsernameEntry.get())
        currentName = sql.GetCurrentFullname(currentUsername)
        return currentName
    
#This subroutine creates the route planner screen
    def CreateRoutePlanner(self):
        self.routePlannerFrame = tk.Frame(self.mainFrame, bg = "Black", width = self.width, height = self.height)
        self.routePlannerFrame.grid(row = 0, column = 0)
        self.routePlannerFrame.grid_propagate(False)

        self.routeBack = tk.Button(self.routePlannerFrame, text = "Back", command = self.RaiseMainMenu)
        self.routeBack.grid(row = 0, column = 0)

        self.frames["RoutePlannerFrame"] = self.routePlannerFrame

#This subroutine creates the station select screen
    def CreateStationSelect(self):
        self.stationSelectFrame = tk.Frame(self.routePlannerFrame, bg = "Pink", width = self.width/2, height = self.height)
        self.stationSelectFrame.grid(row = 1, column = 0)
        self.stationSelectFrame.grid_propagate(False)

        self.SSStartStationLabel = tk.Label(self.stationSelectFrame, bg = "Pink", text = "Start Station")
        self.SSStartStationLabel.grid(row = 0, column = 0)
        self.SSEndStationLabel = tk.Label(self.stationSelectFrame, bg = "Pink", text = "End Station")
        self.SSEndStationLabel.grid(row = 0, column = 3)
        self.SSSpacer = tk.Label(self.stationSelectFrame, bg = "Pink")
        self.SSSpacer.grid(row = 0, column = 2)
        
        self.SSStartScrollbar = tk.Scrollbar(self.stationSelectFrame)
        self.SSEndScrollbar = tk.Scrollbar(self.stationSelectFrame)
        self.SSStartScrollbar.grid(row = 1, column = 1, sticky = "ns")
        self.SSEndScrollbar.grid(row = 1, column = 6, sticky = "ns")
        self.SSStartStationListbox = tk.Listbox(self.stationSelectFrame, yscrollcommand = self.SSStartScrollbar.set)
        self.SSEndStationListbox = tk.Listbox(self.stationSelectFrame, yscrollcommand = self.SSEndScrollbar.set)
        
        self.SSAllStations = sql.GetAllOpenStationNames()
        for i in self.SSAllStations:
            self.SSStartStationListbox.insert(tk.END, str(i))
            self.SSEndStationListbox.insert(tk.END, str(i))
        self.SSStartStationListbox.grid(row = 1, column = 0)
        self.SSEndStationListbox.grid(row = 1, column = 3)
        self.SSStartScrollbar.config(command = self.SSStartStationListbox.yview)
        self.SSEndScrollbar.config(command = self.SSEndStationListbox.yview)
        self.SSStartCurrentSelect = "No Station Selected"
        self.SSEndCurrentSelect = "No Station Selected"
        self.SSStartCurrentStationButton= tk.Button(self.stationSelectFrame, text = "Select Start Station", command = self.StartStationConfirm)
        self.SSStartCurrentStationButton.grid(row = 2, column = 0)
        self.SSEndCurrentStationButton= tk.Button(self.stationSelectFrame, text = "Select End Station", command = self.EndStationConfirm)
        self.SSEndCurrentStationButton.grid(row = 2, column = 3)
        self.SSStartCurrentSelectLabel = tk.Label(self.stationSelectFrame, bg = "Pink", text = "{0}".format(self.SSStartCurrentSelect))
        self.SSEndCurrentSelectLabel = tk.Label(self.stationSelectFrame, bg = "Pink", text = "{0}".format(self.SSEndCurrentSelect))
        self.SSStartCurrentSelectLabel.grid(row = 3, column = 0)
        self.SSEndCurrentSelectLabel.grid(row = 3, column = 3)
        self.SSCalculateRouteButton=tk.Button(self.stationSelectFrame, text = "Go!", command = self.StartSSDijkstra)
        self.SSCalculateRouteButton.grid(row = 1, column = 7)
        self.SSSwitchButton = tk.Button(self.stationSelectFrame, text = "Switch", command = self.SwitchStations)
        self.SSSwitchButton.grid(row = 2, column = 8)
        self.SSStationSelectionStatusLabel = tk.Label(self.stationSelectFrame, bg = "Pink")
        self.SSStationSelectionStatusLabel.grid(row = 1, column = 8)
        self.SSFavouriteButton = tk.Button(self.stationSelectFrame, text = "Favourites", command = self.RaiseFavourites)
        self.SSFavouriteButton.grid(row = 3, column = 8)

        self.frames["StationSelectFrame"] = self.stationSelectFrame

#This subroutine gets the currently highighted value in the start list box and makes it
#the start station
    def StartStationConfirm(self):
        unselected = False
        try:
            startStationSelectIndex = self.SSStartStationListbox.curselection()[0]
        except IndexError:
            unselected = True
        if unselected != True:
            self.SSStartCurrentSelect = str(self.SSStartStationListbox.get(startStationSelectIndex))
            self.SSStartCurrentSelectLabel.config(text = self.SSStartCurrentSelect)
        else:
            pass

#This subroutine gets the currently highighted value in the start list box and makes it
#the start station
    def EndStationConfirm(self):
        unselected = False
        try:
            endStationSelectIndex = self.SSEndStationListbox.curselection()[0]
        except IndexError:
            unselected = True
        if unselected != True:
            self.SSEndCurrentSelect = str(self.SSEndStationListbox.get(endStationSelectIndex))
            self.SSEndCurrentSelectLabel.config(text = self.SSEndCurrentSelect)
        else:
            pass
#This subroutine switches the values of the start and end stations
    def SwitchStations(self):
        startTemp = self.SSStartCurrentSelect
        endTemp = self.SSEndCurrentSelect
        self.SSStartCurrentSelect = endTemp
        self.SSEndCurrentSelect = startTemp
        self.SSStartCurrentSelectLabel.config(text = self.SSStartCurrentSelect)
        self.SSEndCurrentSelectLabel.config(text = self.SSEndCurrentSelect)

#This subroutine gets the start and end station and passes them into the subroutine
#that create the graph and performs Dijkstra's algorithm
    def StartSSDijkstra(self):
        self.ResetRouteInstructions()
        if self.SSStartCurrentSelect == "No Station Selected" or self.SSEndCurrentSelect == "No Station Selected":
            self.SSStationSelectionStatusLabel.config(text = "Start or End Station not selected")
        elif self.SSStartCurrentSelect == self.SSEndCurrentSelect:
            self.SSStationSelectionStatusLabel.config(text = "Start and End Stations are the same")
        else:
            self.SSStationSelectionStatusLabel.config(text = "")
            start = self.SSStartCurrentSelect
            end = self.SSEndCurrentSelect
#This checks to see if the route has alredy been calculated before
            routeExists = sql.CheckIfRouteExists(start, end)
            if routeExists == False:
#This sends the start and end station to the subroutine that starts dijksta's algorithm
                fullRoute = graph.g.CreateStartingNode(start, end)
            else:
#This retrieves the route from the SQL database
                fullRoute = sql.GetExistingRoute(routeExists)
#This displays the total time of the route.
            totalTime = 0
            for i in fullRoute:
                totalTime += i[3]
            self.DisplayRouteInstructions(fullRoute, totalTime)

#This subroutine raises the stataion select screen
    def RaiseStationSelect(self):
        self.currentSelectionFrame = 0
        self.ResetStationSelect()
        self.frames["StationSelectFrame"].tkraise()

#This subroutine resets the station select screen
    def ResetStationSelect(self):
        self.stationSelectFrame.destroy()
        self.CreateStationSelect()

#This subroutine creates the route instructions screen
    def CreateRouteInstructions(self):
        self.routeInsFrame = tk.Frame(self.routePlannerFrame, bg = "Orange", width = self.width/2, height = self.height)
        self.routeInsFrame.grid(row = 1, column = 1)
        self.routeInsFrame.grid_propagate(False)

        self.routeListbox = tk.Listbox(self.routeInsFrame, width = 100, height = 0)
        self.routeListbox.grid(row = 0, column = 0)

        self.frames["RouteInstructionsFrame"] = self.routeInsFrame

#This subroutine displays the instructions taken from the results of the dijkstra's algorithm
    def DisplayRouteInstructions(self, route, time):
        self.generatedRoute = route
        listboxHeight = 0
        stepCounter = 1
        for i in self.generatedRoute:
            self.routeListbox.insert(tk.END, "{0}: {1} to {2} on the {3} line for {4} minutes". format(stepCounter, i[0], i[1], i[2], i[3]))
            listboxHeight += 1
            self.routeListbox.config(height = listboxHeight)
            
            stepCounter += 1
        self.saveInsButton = tk.Button(self.routeInsFrame, text = "Add route to travel plan", command  = self.OpenTravelPlanWindow)
        self.saveInsButton.grid(row = 1, column = 0)
        self.routeFavButton = tk.Button(self.routeInsFrame, text = "Favourite Route", command = self.AddRouteToFavourites)
        self.routeFavButton.grid(row = 2, column = 0)


#This subroutiebe is used to tell the user if the route the set to be favourited exists or not.
    def AddRouteToFavourites(self):
        if self.currentSelectionFrame == 0:
            favExists = sql.AddRouteToFavourites(self.generatedRoute[0][0], self.generatedRoute[-1][1], self.currentUsername)
            if favExists == None:
                favouriteConfimation = tk.Label(self.routeInsFrame, text = "Favourite has been added.")
            else:
                favouriteConfimation = tk.Label(self.routeInsFrame, text = "This route has already been favourited.")
            favouriteConfimation.grid(row = 3, column = 0)

#This subroutine resets the route instructions screen
    def ResetRouteInstructions(self):
        self.routeInsFrame.destroy()
        self.CreateRouteInstructions()

#This subroutine creates the window that allows the user to save instructions to their travel plan
    def OpenTravelPlanWindow(self):
        self.addToTravelPlanWindow = tk.Toplevel(width = 500, height = 200)
        self.addToTravelPlanWindow.grab_set()
        self.addToTravelPlanWindow.title("Add To Travel Plan")

        self.filenameLabel = tk.Label(self.addToTravelPlanWindow, text = "Filename")
        self.filenameLabel.grid(row = 0, column = 0)
        self.filenameEntry = tk.Entry(self.addToTravelPlanWindow)
        self.filenameEntry.grid(row = 0, column = 1)
        self.saveButton = tk.Button(self.addToTravelPlanWindow, text = "Save", command = self.SaveToTravelPlan)
        self.saveButton.grid(row = 1, column = 0, columnspan = 2)
        self.filenameConfirmLabel = tk.Label(self.addToTravelPlanWindow, text = "Please enter a filename")
        self.filenameConfirmLabel.grid(row = 2, column = 0, columnspan = 2)

#This subroutine is used to get the filename that the user entered so it can be used to create a file.
    def SaveToTravelPlan(self):
        self.filename = str(self.filenameEntry.get())
#This section is used to check if there are any special characters in the file name
        if len(self.filename) != 0:
            for character in self.filename:
                if character not in ["(","!","#","£","$","%","&","’","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","\\","]","{","|","}","~",")"]:
                    self.filenameConfirmLabel.destroy()
                    exists = pd.CreateOrEdit(self.filename, self.generatedRoute)
#This section brings up additional options if a file with the same name already exists
                    if exists:
                        self.enteredNameLabel = tk.Label(self.addToTravelPlanWindow, text = self.filename)
                        self.enteredNameLabel.grid(row = 0, column = 1)
                        self.filenameEntry.destroy()
                        self.existsStatusLabel = tk.Label(self.addToTravelPlanWindow, text = "{0} already exists.".format(self.filename))
                        self.existsStatusLabel2 = tk.Label(self.addToTravelPlanWindow, text = "Would you like to overwrite the file or add to it?")
                        self.existsStatusLabel.grid(row = 2, column = 0, columnspan = 3)
                        self.existsStatusLabel2.grid(row = 3, column = 0, columnspan = 3)
                        self.overwriteButton = tk.Button(self.addToTravelPlanWindow, text = "Overwrite", command = self.OverwriteExisting)
                        self.addButton = tk.Button(self.addToTravelPlanWindow, text = "Add", command = self.AddToExisting)
                        self.cancelButton = tk.Button(self.addToTravelPlanWindow, text = "Cancel", command = self.addToTravelPlanWindow.destroy)
                        self.overwriteButton.grid(row = 4, column = 0)
                        self.addButton.grid(row = 4, column = 1)
                        self.cancelButton.grid(row = 4, column = 2)
                    else:
                        self.addToTravelPlanWindow.destroy()
                else:
                    self.filenameConfirmLabel.config(text = "Filename cannot contain any special characters. Please enter a new filename")
        else:
            self.filenameConfirmLabel.config(text = "No filename entered. Please enter a filename")

#This subroutine is used to close the save window once the file has been overwritten
    def OverwriteExisting(self):
        pd.CreateNewDoc(self.filename, "Travel Plans", self.generatedRoute)
        self.addToTravelPlanWindow.destroy()

#This subroutine is used to close the save window once the instructions have been added to the file
    def AddToExisting(self):
        pd.EditExistingDoc(self.filename, "Travel Plans", self.generatedRoute)
        self.addToTravelPlanWindow.destroy()

#This subroutine creates the favourites screen
    def CreateFavourites(self):
        self.favouritesFrame = tk.Frame(self.routePlannerFrame, bg = "Purple", width = self.width/2, height = self.height)
        self.favouritesFrame.grid(row = 1, column = 0)
        self.favouritesFrame.grid_propagate(False)

        self.FFavouritesLabel = tk.Label(self.favouritesFrame, bg = "Purple", text = "Favourite Routes")
        self.FFavouritesLabel.grid(row = 0, column = 0)
        self.FFavouritesScrollbar = tk.Scrollbar(self.favouritesFrame)
        self.FFavouritesListbox = tk.Listbox(self.favouritesFrame, yscrollcommand = self.FFavouritesScrollbar.set, width = 50)
        allFavourites = sql.GetAllFavouriteRouteNames(self.currentUsername)
        for i in allFavourites:
            self.FFavouritesListbox.insert(tk.END, str(i))
        self.FFavouritesListbox.grid(row = 2, column = 0)
        self.FFavouritesScrollbar.config(command = self.FFavouritesListbox.yview)
        self.FFavouritesScrollbar.grid(row = 2, column = 1, sticky = "ns")
        self.FSelectButton = tk.Button(self.favouritesFrame, text = "Select route")
        self.FRouteSelect = "No Route Selected"
        self.FRouteSelectLabel = tk.Label(self.favouritesFrame, bg = "Purple", text = self.FRouteSelect)
        self.FRouteSelectLabel.grid(row = 3, column = 0)
        self.FRouteSelectButton = tk.Button(self.favouritesFrame, text = "Select Route", command = self.SelectFavouriteRoute)
        self.FRouteSelectButton.grid(row = 4, column = 0)
        self.FStationSelectButton = tk.Button(self.favouritesFrame, text = "Station Select", command = self.RaiseStationSelect)
        self.FStationSelectButton.grid(row = 4, column = 2)
        self.FCalculateRouteButton = tk.Button(self.favouritesFrame, text = "Go!", command = self.StartFavouriteCalculation)
        self.FCalculateRouteButton.grid(row = 2, column = 2)
        self.FRouteSelectionStatus = tk.Label(self.favouritesFrame, bg = "Purple", text = "")
        self.FRouteSelectionStatus.grid(row = 2, column = 3)

        self.frames["FavouritesFrame"] = self.favouritesFrame

#This subroutine splits the name of the route so it can be used to perform dikjsta's algorithm
    def StartFavouriteCalculation(self):
        routeDetails = self.FRouteSelect.split(" to ")
        self.StartFDijkstra(routeDetails)

#This subroutine resets the favourites screen
    def ResetFavourites(self):
        self.favouritesFrame.destroy()
        self.CreateFavourites()

#This subroutine raises the favourites screen
    def RaiseFavourites(self):
        self.currentSelectionFrame = 1
        self.ResetFavourites()
        self.frames["FavouritesFrame"].tkraise()

#This subroutine stores the value of the currently selected route in the favourites list box
    def SelectFavouriteRoute(self):
        unselected = False
        try:
            favouritesIndex = self.FFavouritesListbox.curselection()[0]
        except IndexError:
            unselected = True
        if unselected != True:
            self.FRouteSelect = str(self.FFavouritesListbox.get(favouritesIndex))
            self.FRouteSelectLabel.config(text = self.FRouteSelect)
        else:
            pass

#This subroutine confirms that a favourite route has been created and tries to get instructions for that route by
#performing dijkstra's algorithm or getting the details from the database
    def StartFDijkstra(self, routeDetails):
        self.ResetRouteInstructions()
        if self.FRouteSelect == "No Route Selected":
            self.FRouteSelectionStatus.config(text = "No Route Selected")
        else:
            self.FRouteSelectionStatus.config(text = "")
            routeExists = sql.CheckIfRouteExists(routeDetails[0], routeDetails[1])
            if routeExists == False:
                fullRoute = graph.g.CreateStartingNode(routeDetails[0], routeDetails[1])
            else:
                fullRoute = sql.GetExistingRoute(routeExists)
            totalTime = 0
            for i in fullRoute:
                totalTime += i[3]
            self.DisplayRouteInstructions(fullRoute, totalTime)

#This subroutine raises teh route planner
    def RaiseRoutePlanner(self):
        self.ResetRouteInstructions()
        self.ResetFavourites()
        self.ResetStationSelect()
        self.SSStationSelectionStatusLabel.config(text = "")
        self.frames["RoutePlannerFrame"].tkraise()

#This subroutine creates the open close screen
    def CreateOpenClose(self):
        self.openCloseFrame = tk.Frame(self.mainFrame, bg = "Lime Green", width = self.width, height = self.height)
        self.openCloseFrame.grid(row = 0, column = 0)
        self.openCloseFrame.grid_propagate(False)
        self.openCloseBackButton = tk.Button(self.openCloseFrame, text = "Back", command = self.RaiseMainMenu)
        self.openCloseBackButton.grid(row = 0, column = 0)
        self.openCloseAllStations = sql.GetAllStationsStatus()

        self.openCloseScrollbar = tk.Scrollbar(self.openCloseFrame)
        self.openCloseTable = ttk.Treeview(self.openCloseFrame, height = 25, columns = "openClose", yscrollcommand = self.openCloseScrollbar.set)
        self.openCloseTable.grid(row = 1, column = 0)
        self.openCloseScrollbar.grid(row = 1, column = 1, sticky = "ns")
        self.openCloseScrollbar.config(command = self.openCloseTable.yview)
        self.openCloseTable.heading("#0", text = "Station Name")
        self.openCloseTable.heading("openClose", text = "Open / Close")

        allStationValues = []
        allIDs = sql.GetAllStationIDs()
        noStations = 0
        for i in allIDs:
            noStations+=1
        print("No. of stations in table = {0}".format(noStations))
        for ID in allIDs:
            stationValues = []
            name = sql.GetStationName(ID)
            status = sql.GetStationStatus(name)
            stationValues.append(ID)
            stationValues.append(name)
            stationValues.append(status)
            allStationValues.append(stationValues)

        for station in allStationValues:
            self.openCloseTable.insert("", "end", "{0}".format(station[0]), text = "{0}".format(station[1]))
            if station[2] == 0:
                self.openCloseTable.set("{0}".format(station[0]), "openClose", "Closed")
            else:
                self.openCloseTable.set("{0}".format(station[0]), "openClose", "Open")
            self.openCloseTable.bind("<<TreeviewSelect>>", self.UpdateOpenCloseValue)
            
        self.frames["OpenCloseFrame"] = self.openCloseFrame

#this subroutine raises the open close screen
    def RaiseOpenClose(self):
        self.frames["OpenCloseFrame"].tkraise()

#this subroutine changes the text of a station's status from open to closed or vice versa and then passes some information on to the SQL database
    def UpdateOpenCloseValue(self, event):
        ID = self.openCloseTable.selection()
        ID = ID[0]
        status = sql.GetStationStatusFromID(ID)
        if status == 0:
            self.openCloseTable.set("{0}".format(ID), "openClose", "Open")
            newStatus = 1
        else:
            self.openCloseTable.set("{0}".format(ID), "openClose", "Closed")
            newStatus = 0
        sql.UpdateOpenCloseValue(ID, newStatus)

#This subroutine gets a picture of the London Underground map and then displays it in a window
    def OpenMapFile(self):
        if PILImportSuccess == True:
            if self.mapOpen == 0:
                mapPhotoLoad = Image.open("london-tube-map.png")
                self.mapPhoto = ImageTk.PhotoImage(mapPhotoLoad)
                self.photoWindow = tk.Toplevel(width = 500, height = 350)
                self.photoWindow.attributes("-topmost", "true")
                self.photoWindow.title("Map")
                self.photoWindow.protocol("WM_DELETE_WINDOW", self.ClosingMapWindow)
                
                self.photoYScroll = tk.Scrollbar(self.photoWindow)
                self.photoYScroll.grid(row = 0, column = 1, sticky = "ns")
                self.photoXScroll = tk.Scrollbar(self.photoWindow, orient = tk.HORIZONTAL)
                self.photoXScroll.grid(row = 1, column = 0, sticky = "ew")
                self.photoCanvas = tk.Canvas(self.photoWindow, width = 500, height = 350)
                self.photoCanvas.create_image(0,0, image = self.mapPhoto)
                self.photoCanvas.config(scrollregion = self.photoCanvas.bbox(tk.ALL), yscrollcommand = self.photoYScroll.set, xscrollcommand = self.photoXScroll.set)
                self.photoCanvas.grid(row = 0, column = 0)
                self.photoYScroll.config(command = self.photoCanvas.yview)
                self.photoXScroll.config(command = self.photoCanvas.xview)
                self.mapOpen = 1

#This subroutine handles closing the map screen so multiple windows cannot be open at a time.
    def ClosingMapWindow(self):
        self.mapOpen = 0
        self.photoWindow.destroy()
app = GUI()
