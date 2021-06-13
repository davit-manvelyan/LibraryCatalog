import configparser

class Books:

    def __init__(self, booksList):
        self.booksList = booksList

    def add_book(self, bookID, title, copies, available_copies):
        self.booksList[bookID] = {"title": title,
                                  "copies" : copies,
                                  "available copies" : available_copies}
        with open("books.ini", "w") as booksDB:
            self.booksList.write(booksDB)
        print("The Book has successfully been added. \n\n")

    def remove_book(self, bookID):
        self.booksList.remove_section(bookID)
        with open("books.ini", "w") as booksDB:
            self.booksList.write(booksDB)
        print("The book has been removed. \n\n")

    def check_book_availability(self, title):
        bookID = ""
        for i in self.booksList.sections():
            if title == self.booksList[i]['title']:
                bookID = i
                break
        if bookID == "":
            print("The book is not in library \n\n")
        elif int(self.booksList[bookID]["available copies"]) > 0:
           print("There is available {} copies. \n\n".format(self.booksList[bookID]["available copies"]))
           #return int(self.booksList[bookID]["available copies"])
        else:
            print("The book is not available right now. You can reserve it. \n\n")
            #return int(self.booksList[bookID]["available copies"])
