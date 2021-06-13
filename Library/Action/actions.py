import configparser
import datetime

class Actions:

    def __init__(self, actionsList, usersList, booksList):
        self.actionsList = actionsList
        self.usersList = usersList
        self.booksList = booksList

    def user_checkout_book(self, actionID, userID, bookID, returnDate, status):
        self.actionsList[actionID] = {"userID" : userID, "bookID" : bookID, "return date" : returnDate, "status" : status}
        with open("actions.ini", "w") as actions:
            self.actionsList.write(actions)
        self.booksList.set(bookID, "available copies", str(int(self.booksList[bookID]["available copies"]) - 1))
        with open("../Book/books.ini", "w") as books:
            self.booksList.write(books)
        print("The book has been sucssecfully checked out: \n\n")


    def user_return_book(self, actionID, returnDate, status):
        self.booksList.set(self.actionsList[actionID]["bookID"],"available copies",
                           str(int(self.booksList[self.actionsList[actionID]["bookID"]]["available copies"]) + 1))
        with open("../Book/books.ini", "w") as books:
            self.booksList.write(books)

        bookID = self.actionsList[actionID]["bookID"]

        must_re_date = self.actionsList[actionID]["return date"].split("-") # [2021,9,11]
        ret_date = returnDate.split("-")                                    # [2021,6,13]
        diff = (datetime.date(int(ret_date[0]), int(ret_date[1]), int(ret_date[2])) - datetime.date(int(must_re_date[0]), int(must_re_date[1]), int(must_re_date[2])))
        if diff.days > 7:
            print("Your fine is {} dollars".format(diff.days // 7 * 5))

        subscribers = []
        if int(self.booksList[bookID]["available copies"]) == 1:
            for i in self.actionsList.sections():
                if bookID == self.actionsList[i]["bookID"] and self.actionsList[i]["status"] == "reserved":
                    subscribers.append(self.usersList[self.actionsList[i]["userID"]]["name"])

        if len(subscribers) > 0:
            print(subscribers)

        self.actionsList.remove_section(actionID)
        with open("actions.ini", "w") as actions:
            self.actionsList.write(actions)
        print("User has returned book")

    def users_who_have_given_book(self, bookID, status):
        lst = []
        for actionID in self.actionsList.sections():
            if bookID == self.actionsList[actionID]["bookID"] and status == self.actionsList[actionID]["status"]:
                lst.append(self.usersList[self.actionsList[actionID]["userID"]]["name"])
        if lst == []:
            print("NO users for current book or the name of book is not right")
        else:
            print(lst)

    def reserved(self,actionID,  userID, bookID, status):
        self.actionsList[actionID] = {"userID" : userID, "bookID" : bookID, "status" : status}
        with open("actions.ini", "w") as actions_DB:
            self.actionsList.write(actions_DB)

    def subscribers_of_the_book(self, bookID, status):
        userList = []
        for i in self.actionsList.sections():
            if bookID == self.actionsList[i]["bookID"] and status == self.actionsList[i]["status"]:
                userList.append(self.usersList[self.actionsList[i]["userID"]]["name"])

        if len(userList) != 0:
            print(userList)
        else:
            print("Subscribers is not exist")


    def overdue_books_of_the_user(self, userID, status, returnDate):
        books = []
        for i in self.actionsList.sections():
            if userID == self.actionsList[i]["userID"] and status == self.actionsList[i]["status"]:
                action_return_date = self.actionsList[i]["return date"].split("-")
                retrunDate_actual = returnDate.split("-")
                diff = (datetime.date(int(retrunDate_actual[0]), int(retrunDate_actual[1]), int(retrunDate_actual[2])) - datetime.date(int(action_return_date[0]), int(action_return_date[1]), int(action_return_date[2])))
                if diff.days > 0:
                    books.append(books[self.actionsList[i]["bookID"]]["title"])
        if len(books) != 0:
            print(books)
        else:
            print("User doesn't have overdue books")

    def fine_for_overdue(self, userID, bookID, status, returnDate):
        fine = 0
        for i in self.actionsList.sections():
            if userID == self.actionsList[i]["userID"] and bookID == self.actionsList[i]["bookID"] and status == self.actionsList[i]["status"]:
                actual_return_date = self.actionsList[i]["return date"].split("-")
                now = returnDate.split("-")
                diff = (datetime.date(int(now[0]), int(now[1]), int(now[2])) - datetime.date(int(actual_return_date[0]), int(actual_return_date[1]), int(actual_return_date[2])))
                if diff.days > 7:
                    fine = diff.days // 7 * 5
        if fine > 0:
            print("Your fine is {}$".format(fine))
        else:
            print("There is no fine for current data")

    def total_fine_for_overdue(self, userID, status, returnDate):
        sum_of_fine = 0
        for i in self.actionsList.sections():
            fine = 0
            if userID == self.actionsList[i]["userID"] and status == self.actionsList[i]["status"]:
                actual_return_date = self.actionsList[i]["return date"].split("-")
                now = returnDate.split("-")
                diff = (datetime.date(int(now[0]), int(now[1]), int(now[2])) - datetime.date(int(actual_return_date[0]), int(actual_return_date[1]), int(actual_return_date[2])))
                if diff.days > 7:
                    fine = diff.days // 7 * 5
                    sum_of_fine += fine
        if sum_of_fine > 0:
            print("Your fine is {} $".format(sum_of_fine))
        else:
            print("There is no fine for current data")