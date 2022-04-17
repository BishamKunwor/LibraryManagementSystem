from datetime import date, datetime


# fileName is the file from which library book database is read and stored.
stockFileName = "stock.txt"

bookRecords = []

# bookRecords Contains list of dictionary as
# {"Name": "Intro To Java", "Author/s": "Bisham Kunwor",
#                                 "Available": 20, "Price": 1}

# sNo is used to temporarily index the available books in the table
sNo = 1


def appendInbookRecords(bookName, authorName, booksAvailable, price):
    """Appends a dictonary containing bookName, authorName, booksAvailable and price in bookRecords List."""
    bookRecords.append({"Name": bookName, "Author/s": authorName,
                        "Available": booksAvailable, "Price": price})


def fileExists(fileName):
    """Returns True if fileName text file exist else returns false"""
    try:
        with open(fileName) as dbfile:
            pass
        return True

    except FileNotFoundError:
        return False


def addBookRecords(fileName):
    """Adds all the record as dictonary in the bookRecords list from fileName text file."""
    with open(fileName) as dbFile:
        data = dbFile.readlines()

    # The loop splits all the record into a list containg Name, Author, Total Available Number, Price in index 0,1,2,3 respectively
    for record in data:
        if record == '\n':
            continue
        try:
            record = record[:record.index("\n")]
        except:
            pass
        bookInfo = record.split(",")

        bookRecords.append({"Name": bookInfo[0], "Author/s": bookInfo[1],
                            "Available": int(bookInfo[2]), "Price": float(bookInfo[3][1:])})


def readFile(fileName):
    """Extracts all the data from fileName text file to bookRecords list if fileName text file exist."""
    if fileExists(fileName):
        addBookRecords(fileName)


def printBookTable():
    """Prints all the books information in tabluar form contained in the bookRecords global valiable."""
    print(
        f"Available Books\n\n{'S.N.':<10} {'Name':<40} {'Author/s':<50} {'Stocks Available':<30} {'Price':<2}\n")

    global sNo
    # sNo is used to temporarily index the available books in the table
    sNo = 1
    # This loop prints all the books information from bookRecords list
    for record in bookRecords:
        print(
            f"{sNo:<10} {record['Name']:<40} {record['Author/s']:<50} {record['Available']:<30} ${record['Price']:<2}")
        sNo += 1


def stringValidator(inputMessage, errForLenMsg):
    """Validates length of string to be greater than 2 and prompts user until a valid string is provided."""
    while True:
        strName = input(inputMessage)
        if strName:
            if len(strName) > 2:
                return strName
            else:
                print(errForLenMsg)
        else:
            print("Please enter something.")


def numChecker(inputMsg, exceptionErrMsg="Please Enter a number.", conditionFunction=lambda x: "Passed"):
    """Checks if a number is Provided and it is greater than 0. Also prompts user until a valid number is provided"""
    while True:
        try:
            number = int(input(inputMsg))
            if number > 0:
                # runs conditionFunction which returns "Passed" or None
                if conditionFunction(number) == "Passed":
                    return number
            else:
                print("Please enter a valid number.")
        except ValueError:
            print(exceptionErrMsg)


def addBookInfo():
    """Adds (appends) new book on the bookRecords list."""

    bookName = stringValidator(
        "Enter Name of the book: ", "The Book Name is not valid.")

    authorsName = stringValidator(
        "Enter Author/s of the book: ", "The name of the author is not valid.")

    availableBooks = numChecker("Enter books available for borrowing: ",
                                "Please use numbers to represent stock available.")

    price = numChecker("Enter Price of the book: ",
                       "Please use numbers to represent price of the book.")

    appendInbookRecords(
        bookName=bookName, authorName=authorsName, booksAvailable=availableBooks, price=float(price))
    print(f"{bookName} written by {authorsName} was added with the price of ${price} and availability of {availableBooks}.")
    input("Press Enter to continue.")


def sNoChecker(bookNumber):
    if bookNumber < sNo:
        return "Passed"
    print(
        "Please Enter a valid S.N. of the book.")


def lendBook():

    totalBookToLend = numChecker(
        "Enter how many books to lend: ")

    # booksData holds the name, books and total price for a user lending book
    booksData = {"Name": None,
                 "Books": [], "Total Price": 0}

    booksData["Name"] = stringValidator(
        "Enter your name: ", "The name is not valid.")

    # The loop checks if the book is available or not and it is available then lends it to the user and reduces the availability of the book by one
    for repetion in range(totalBookToLend):
        bookNumber = numChecker(
            inputMsg="Enter S.N. of book to borrow: ", conditionFunction=sNoChecker)

        if bookRecords[bookNumber-1]['Available'] == 0:
            print("Book is not available at the moment.")
            input("Press Enter to continue.")
        else:
            bookRecords[bookNumber -
                        1]['Available'] -= 1

            booksData["Books"].append(
                bookRecords[bookNumber-1]['Name'])
            booksData["Total Price"] += bookRecords[bookNumber-1]['Price']

            print(
                f"{bookRecords[bookNumber-1]['Name']} was borrowed.")

    # checks if user has selected some book and writes it to borrow database
    if len(booksData["Books"]) != 0:
        # uid is unique id for indivisual user
        uid = str(datetime.now())
        uid = uid[-6:] + uid[:4] + uid[-8:-9] + uid[-11:-10]
        with open("borrowDatabase.txt", "a") as dbFile:
            dataToWrite = f"{booksData['Name']}"
            for book in booksData["Books"]:
                dataToWrite += ","
                dataToWrite += f"{book}"
            dbFile.write(
                f"{dataToWrite},{date.today()},${booksData['Total Price']},{uid}\n")
        # print(f"Total Price: {booksData['Total Price']}\n")
        if len(booksData["Books"]) == 1:
            print(
                f"{booksData['Name']} brought {booksData['Books'][0]} at total price of ${booksData['Total Price']}.\n")
            print(f"UID for the borrowed books: {uid}")
        elif len(booksData["Books"]) == 2:
            print(
                f"{booksData['Name']} brought {booksData['Books'][0]} and {booksData['Books'][1]} at the total price of ${booksData['Total Price']}\n")
            print(f"UID for the borrowed books: {uid}")
        elif len(booksData["Books"]) > 2:
            tempStr = f"{booksData['Name']} bought "
            for count in range(len(booksData["Books"])):
                tempStr += f"{booksData['Books'][count]}, "
                if count == len(booksData["Books"]) - 2:
                    tempStr += "and "
            tempStr += f"at the total price of ${booksData['Total Price']}.\n"
            print(tempStr)
            print(f"UID for the borrowed books: {uid}")

        input("Press Enter to continue.")

    if len(bookRecords) != 0:
        with open("stock.txt", "w") as dbFile:
            for record in bookRecords:
                dbFile.write(
                    f"{record['Name']},{record['Author/s']},{record['Available']},${record['Price']}\n")


def returnBook():

    totalBookToRecieve = numChecker(
        inputMsg="Enter how many books to return: ")

    # booksData holds the name, books and fined price for a user returning book
    booksData = {"Name": None,
                 "Books": [], "Fine Price": 0}

    booksData["Name"] = stringValidator(
        "Enter borrower's name: ", "The name is not valid.")
    borrowDatabase = []

    # Try block tries to read borrowDatabase.txt file and if it does not exist then runs the exception of data not found in database.
    try:
        with open("borrowDatabase.txt") as history:

            data = history.readlines()
            # The loops reads each line record of borrowDatabse and appends a dictonary with name, booklist, data and total price of books
            for record in data:
                if record == '\n':
                    continue
                try:
                    record = record[:record.index("\n")]
                except:
                    pass
                bookInfo = record.split(",")

                if bookInfo[-3][5] == "0":
                    month = bookInfo[-3][6]
                else:
                    month = bookInfo[-3][5:7]

                if bookInfo[-3][8] == "0":
                    dayValue = bookInfo[-3][9]
                else:
                    dayValue = bookInfo[-3][8:]

                dayValue = int(dayValue)
                month = int(month)
                dated = date(int(bookInfo[-3][:4]),
                             month, dayValue)

                booksList = [book for book in bookInfo[1:-3]]

                borrowDatabase.append({"Name": bookInfo[0], "Books": booksList,
                                       "Date": dated, "Total Price": float(bookInfo[-2][1:]), "UID": bookInfo[-1]})
    except FileNotFoundError:
        print("No records found in database.")
        input("Press enter to continue.")
    else:
        uid = None
        uidFoundInDatabase = False
        uidFoundIndex = None
        while True:
            uid = input("Enter UID: ")
            if uid:
                for userDetails in borrowDatabase:
                    if userDetails["UID"] == uid:
                        uidFoundInDatabase = True
                        uidFoundIndex = borrowDatabase.index(userDetails)
                break
            else:
                print("Empty UID Found.")
                input("Press Enter to continue.")

        if uidFoundInDatabase:
            for repetion in range(totalBookToRecieve):
                bookNumber = numChecker(
                    "Enter S.N. of book to recieve: ", conditionFunction=sNoChecker)

                # Checks if the book is present in the database
                if bookNumber in range(1, sNo+1):
                    booksData["Books"].append(
                        bookRecords[bookNumber-1]['Name'])

            finePriceFrMultiBooks = 0
            for book in booksData["Books"]:

                if len(borrowDatabase[uidFoundIndex]["Books"]) == 1:

                    if book in borrowDatabase[uidFoundIndex]["Books"]:
                        appliedFineDays = date.today(
                        ) - borrowDatabase[uidFoundIndex]["Date"]
                        try:
                            appliedFineDays = int(
                                str(appliedFineDays).split()[0])
                        except ValueError:
                            appliedFineDays = 10

                        if appliedFineDays > 10:
                            booksData['Fine Price'] = (
                                appliedFineDays - 10)*borrowDatabase[uidFoundIndex]["Total Price"]*0.05

                        print(
                            f"Total Fine for {book}: ${booksData['Fine Price']:.2f}")

                        while True:
                            userChoice = input(
                                "Would you like to proceed to transaction. (y/n) ")
                            if userChoice:
                                userChoice = userChoice[0].lower()
                                if userChoice == "y":
                                    for data in bookRecords:
                                        if data["Name"] == book:
                                            data["Available"] += 1
                                            print(
                                                f"{data['Name']} was recieved.")
                                    with open("recieveDatabase.txt", "a") as file:
                                        file.write(
                                            f"{booksData['Name']},{book},{date.today()},${booksData['Fine Price']},{uid}\n")
                                    borrowDatabase.pop(uidFoundIndex)
                                    break
                                elif userChoice == "n":
                                    break
                                else:
                                    print("Please Enter valid option")
                                    input("Press Enter to continue.")
                            else:
                                print("Please Enter something.")
                                input("Press Enter to continue.")
                    else:
                        print(
                            "Sorry, The book is not found in the borrowed database.")

                else:
                    if book in borrowDatabase[uidFoundIndex]["Books"]:
                        appliedFineDays = date.today(
                        ) - borrowDatabase[uidFoundIndex]["Date"]

                        for data in bookRecords:
                            if data["Name"] == book:
                                price = data["Price"]
                        try:
                            appliedFineDays = int(
                                str(appliedFineDays).split()[0])
                        except ValueError:
                            appliedFineDays = 10

                        if appliedFineDays > 10:

                            finePriceFrMultiBooks = (
                                appliedFineDays - 10)*price*0.05

                        print(
                            f"Total Fine for {book}: ${finePriceFrMultiBooks:.2f}")

                        while True:
                            userChoice = input(
                                "Would you like to proceed to transaction. (y/n) ")
                            if userChoice:
                                userChoice = userChoice[0].lower()
                                if userChoice == "y":
                                    for data in bookRecords:
                                        if data["Name"] == book:
                                            data["Available"] += 1
                                            print(
                                                f"{data['Name']} was recieved.")

                                    with open("recieveDatabase.txt", "a") as file:
                                        file.write(
                                            f"{booksData['Name']},{book},{date.today()},${booksData['Fine Price']},{uid}\n")

                                    borrowDatabase[uidFoundIndex]["Books"].remove(
                                        book)

                                    break
                                elif userChoice == "n":
                                    break
                                else:
                                    print("Please Enter valid option")
                                    input("Press Enter to continue.")
                            else:
                                print("Please Enter something.")

                                input("Press Enter to continue.")
                    else:
                        print(
                            "Sorry, The book is not found in the borrowed database.")

                with open("borrowDatabase.txt", "w") as file:
                    for data in borrowDatabase:
                        dataToWrite = f"{data['Name']}"
                        for books in data["Books"]:
                            dataToWrite += ","
                            dataToWrite += f"{books}"
                        file.write(
                            f"{dataToWrite},{data['Date']},${data['Total Price']},{uid}\n")

            input("Press Enter to continue.")
        else:
            print("Sorry, the provided UID does not have borrow history in the database.")
            input("Press Enter to continue. ")

        if len(bookRecords) != 0:
            with open("stock.txt", "w") as dbFile:
                for record in bookRecords:
                    dbFile.write(
                        f"{record['Name']},{record['Author/s']},{record['Available']},${record['Price']}\n")


def adminFunction():
    """"Prints all the available books on the stock.txt file.
    All the administrativie decission to quit, lend, return books are handeled by this function."""

    print("""
    Welcome To Our Library Management System
    ----------------------------------------
    """)

    # Program doesn't quits until administrator decides to do so
    while True:

        printBookTable()

        print(
            "\n\nl - (lend books)\nr - (return a book)\na - (add book details)\nd - (delete book details)\nq - (quits the program)\n(Enter to refresh)\n\n")

        quitChoice = input("Enter your choice: ")

        # This code runs if some character is typed else the while loop continues and displays all the information again when Enter is pressed
        if quitChoice:
            choice = quitChoice[0].lower()

            # This if statement writes book data in file if bookRecords contains book information and if bookRecords is empty then does nothing
            if choice == "q":

                print("""
                Thanks For Using Our Library Management System
                ----------------------------------------------
                """)
                break

            # This block of code runs addBookInfo function which adds new book that is available for borrowing
            elif choice == "a":
                addBookInfo()

            # This block of code deletes any book that the organization decides not to issue
            elif choice == "d":
                while True:
                    try:
                        deleteId = int(
                            input("Enter S.N. of the book record to be deleted: "))
                        if deleteId < sNo and deleteId > 0:
                            input(
                                f"{bookRecords[deleteId-1]['Name']} was deleted.\nPress Enter to continue.")
                            bookRecords.pop(deleteId-1)
                        else:
                            print("Please Enter a valid number.")
                            input("Press Enter to continue: ")
                        break
                    except ValueError:
                        print("Please Enter a number.")

            # This block of code runs lendBook function which handls all data related to book borrowing
            elif choice == 'l':
                lendBook()

            # This block of code runs returnBook function which handls all data related to book recieving
            elif choice == "r":
                returnBook()

            # This block of code runs and warns user if an invalid option is selected
            else:
                print("Invalid option selected. Please Try again.")
                input("Press Enter to continue.")


def main():
    """Program execution starts here."""
    readFile(stockFileName)
    adminFunction()


if __name__ == "__main__":
    main()
