from User.users import Users
from Book.books import Books
from Action.actions import Actions
import configparser
import datetime
import random


if __name__ == '__main__':

    config_user = configparser.ConfigParser()
    config_user.read("users.ini")
    user = Users(config_user)

    config_book = configparser.ConfigParser()
    config_book.read("books.ini")
    book = Books(config_book)

    config_action = configparser.ConfigParser()
    config_action.read("actions.ini")
    action = Actions(config_action, config_user, config_book)

    while True:
        choose = input("\n\nChoose an action:\n "
                       "1: Add user \n "
                       "2: Remove user \n "
                       "3: Add Book \n "
                       "4: Remove Book \n "
                       "5: Check book availability \n "
                       "6: User Checkout book \n "
                       "7: User return book \n "
                       "8: User reserve book \n"
                       "9: Users who have given book \n"
                       "10: Subscribers of the book \n"
                       "11: Overdue books of the user \n"
                       "12: Fine for overdue \n"
                       "13: Total fine of the user \n"
                       "-1: Exit \n\n\n"
                       "Enter action number: ")

        if choose == "1":
            while True:
                userID = str(random.randint(1,10000))
                if userID in config_user.sections():
                    continue
                else:
                    break

            name = input("Enter Name Surname (eg. John Smith):")
            user.add_user(userID, name)

        elif choose == "2":
            while True:
                userID = input("Enter User ID (eg.005): ")
                if userID.isdigit() and userID in config_user.sections():
                    break
                else:
                    print("Enter valid info!!! \n")

            user.remove_user(userID)

        elif choose == "3":
            while True:
                bookID = input("Enter bookID (eg.005): ")
                title = input("Enter Title of the book:")
                copies = input("Enter Number of copies: ")
                available_copies = copies

                if bookID.isdigit() and copies.isdigit() and bookID not in config_book.sections():
                    book.add_book(bookID, title, copies, available_copies)
                    break
                else:
                    print("Please enter valid information!!! \n")

        elif choose == "4":
            while True:
                bookID = input("Enter bookID (eg.0125):")
                if bookID.isdigit() and bookID in config_book.sections():
                    book.remove_book(bookID)
                    break
                else:
                    print("Please enter valid information!!!! \n")

        elif choose == "5":
                title = input("Enter Title of the book:")
                book.check_book_availability(title)


        elif choose == "6":
            while True:
                actionID = random.randint(1, 10000)
                userID = input("Enter User ID:")
                bookID = input("Enter Book ID:")
                if int(config_book[bookID]["available copies"]) < 1:
                    print("Book is not available")
                    continue
                status = "checkout"
                if actionID not in config_action.sections() and userID in config_user.sections() and\
                        bookID in config_book.sections() and userID.isdigit() and bookID.isdigit():
                    r_date = datetime.datetime.now() + datetime.timedelta(days=90)
                    returnDate = "{}-{}-{}".format(r_date.year, r_date.month, r_date.day) # 2021-06-13
                    action.user_checkout_book(actionID, userID, bookID, returnDate, status)
                    break
                else:
                    print("Please enter valid information")


        elif choose == "7":
            while True:
                actionID = input("Enter action ID:")
                status = "reserved"
                if actionID in config_action.sections() and actionID.isdigit():
                    now = datetime.datetime.now()
                    returnDate = "{}-{}-{}".format(now.year, now.month, now.day) # 2021-06-13
                    action.user_return_book(actionID, returnDate, status)
                    break
                else:
                    print("Please enter valid info \n")


        elif choose == "8":
            bookID = ""
            isExist = False
            while True:
                actionID = random.randint(1, 10000)
                title = input("Enter book title: ")
                userID = input("Enter user id: ")

                for i in config_book.sections():
                    if title == config_book[i]["title"]:
                        isExist = True
                        bookID = i
                        break
                if isExist == False:
                    print("Book is not exist")
                    break
                status = "reserved"
                if userID in config_user.sections() and userID.isdigit() and actionID not in config_action.sections():
                    action.reserved(actionID, userID, bookID, status)
                    break
                else:
                    print("Please enter valid info")


        elif choose == "9":
            title = input("Enter Title of the book: ")
            status = 'checkout'
            isExist = False
            for bookID in config_book.sections():
                if title == config_book[bookID]['title']:
                    action.users_who_have_given_book(bookID, status)
                    isExist = True
                    break
            if isExist == False:
                print("There is no book with that title")

        elif choose == "10":
            title = input("Enter the title of the book: ")
            status = "reserved"
            isExist = False
            for bookID in config_book.sections():
                if title == config_book[bookID]["title"]:
                    action.subscribers_of_the_book(bookID, status)
                    isExist = True
                    break

            if isExist == False:
                print("There is no book with that title")


        elif choose == "11":
            status = "checkout"
            while True:
                userID = input("Enter user ID: ")
                returnDate_actual = datetime.datetime.now()
                returnDate = "{}-{}-{}".format(returnDate_actual.year, returnDate_actual.month, returnDate_actual.day)

                if userID.isdigit() and userID in config_user.sections():
                    action.overdue_books_of_the_user(userID, status, returnDate)
                    break
                else:
                    print("Please enter valid info")

        elif choose == "12":
            status = "checkout"
            now = datetime.datetime.now()
            returnDate = "{}-{}-{}".format(now.year, now.month, now.day)
            while True:
                userID = input("Enter user ID: ")
                bookID = input("Enter book ID: ")

                if userID.isdigit() and bookID.isdigit() and userID in config_user.sections() and bookID in config_book.sections():
                    action.fine_for_overdue(userID, bookID, status, returnDate)
                    break
                else:
                    print("Enter valid info!!! \n\n")

        elif choose == "13":
            status = "checkout"
            now = datetime.datetime.now()
            returnDate = "{}-{}-{}".format(now.year, now.month, now.day)
            while True:
                userID = input("Enter user ID: ")
                if userID.isdigit() and userID in config_user.sections():
                    action.total_fine_for_overdue(userID, status, returnDate)
                    break
                else:
                    print("Enter valid info!!! \n\n")

        elif choose == "-1":
            exit()

        else:
            print("Please enter valid action:")




