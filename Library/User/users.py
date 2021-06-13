import configparser

class Users:

    def __init__(self, usersList):
        self.usersList = usersList

    def add_user(self, userID, name):
        self.usersList[userID] = {"name": name}
        with open("users.ini", "w") as usersDB:
            self.usersList.write(usersDB)
        print("The user has been successfully added to database. \n\n")

    def remove_user(self, userID):
        self.usersList.remove_section(userID)
        with open("users.ini", "w") as usersDB:
            self.usersList.write(usersDB)
        print("The user has been removed from database. \n\n")

