from tkinter import *
import tkinter as tkp
from tkinter import ttk
from ttkthemes import themed_tk as tk
import sqlite3
from sosGUI import *

l1 = []
sqliteConnection = sqlite3.connect('sosgame.sqlite')
cursor = sqliteConnection.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS main(
    name  CHAR  NOT NULL,
    family  CHAR NOT NULL,
    username  CHAR  UNIQUE  PRIMARY KEY,
    password  CHAR  NOT NULL,
    plays INT DEFAULT 0,
    wins INT DEFAULT 0
);
''')

print("successfully connected to the DB.")


def insert(name, family, username, password):
    try:
        sqlite_insert_query = """INSERT INTO main
                              (name, family, username, password)
                               VALUES
                              (?,?,?,?)"""

        data_tuple = (name, family, username, password)
        cursor.execute(sqlite_insert_query, data_tuple)
        sqliteConnection.commit()
        print("inserted successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data.", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("closed")


def select(username, password):
    try:
        sqliteConnection = sqlite3.connect('sosgame.sqlite')
        cursor = sqliteConnection.cursor()
        #print("successfully connected to read.")
        sql_select_query = """select * from main where username = ? and password = ?"""
        cursor.execute(sql_select_query, (username, password))
        records = cursor.fetchall()
        l1.append(records)
        for row in records:
            if password == row[3] and username == row[2]:
                menu()
                login_info(records)

            else:
                labelreq = Label(root, text="Username or password is not correct!")
                labelreq.grid(row=4, column=0)
        cursor.close()

    except sqlite3.Error as error:
        print("failed to insert", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            #print("closed")


# window
root = tk.ThemedTk()
root.set_theme("black")
root.title("MENU")
root.geometry("500x300")


def login_info(records):
    newWindow = Toplevel(root)
    newWindow.title("LOGIN INFO")
    newWindow.geometry("400x400")
    for row in records:
        labelreq1 = Label(newWindow, text="First name : %s" % (row[0]))
        labelreq1.grid(row=0, column=0)
        labelreq2 = Label(newWindow, text="Last name : %s" % (row[1]))
        labelreq2.grid(row=1, column=0)
        labelreq3 = Label(newWindow, text="Username : %s" % (row[2]))
        labelreq3.grid(row=2, column=0)
        labelreq4 = Label(newWindow, text="password : %s" % (row[3]))
        labelreq4.grid(row=3, column=0)
        labelreq5 = Label(newWindow, text="That was your submitted info.")
        labelreq5.grid(row=4, column=0)


def gameWindow():
    select(entry1.get(), entry2.get())


def openNewWindow():
    def show():
        insert(entry5.get(), entry6.get(), entry7.get(), entry8.get())
    try:
        if entry3.get() == 'admin' and entry4.get() == '123456':
            newWindow = Toplevel(root)
            newWindow.title("CREATE ACCOUNT")
            newWindow.geometry("400x400")
            label5 = tkp.Label(newWindow, text="First name")
            label6 = tkp.Label(newWindow, text="Last name")
            label7 = tkp.Label(newWindow, text="Username")
            label8 = tkp.Label(newWindow, text="Password")
            entry5 = tkp.Entry(master=newWindow, width=25)
            entry6 = tkp.Entry(master=newWindow, width=25)
            entry7 = tkp.Entry(master=newWindow, width=25)
            entry8 = tkp.Entry(master=newWindow, width=25)

            label5.grid(row=0, column=0)
            label6.grid(row=1, column=0)
            label7.grid(row=2, column=0)
            label8.grid(row=3, column=0)

            entry5.grid(row=0, column=1)
            entry6.grid(row=1, column=1)
            entry7.grid(row=2, column=1)
            entry8.grid(row=3, column=1)

            finishbtn = ttk.Button(newWindow, text="Submit", command=show)
            finishbtn.grid(row=4, column=0)

        else:
            labelreq = Label(root, text="SOMTHING IS WRONG!")
            labelreq.grid(row=9, column=0)
    except(RuntimeError, TypeError, NameError, OSError) :
        print('Error')


#def addPlayedGame(username):
#    cursor = sqliteConnection.cursor()
#    query = "UPDATE main SET plays = plays + 1 WHERE username = '%s'" % username
#    try:
#        cursor.execute(query)
#        sqliteConnection.commit()
#        print('added a played game to', username)
#        return True
#    except:
#        sqliteConnection.rollback()
#        print('failed to add game')
#        return False


#def addWonGame(username):
#    cursor = sqliteConnection.cursor()
#    query = "UPDATE main SET wins = wins + 1 WHERE username = '%s'" % username
#    try:
#        cursor.execute(query)
#        sqliteConnection.commit()
#        print('added a win game to', username)
#        return True
#    except:
#        sqliteConnection.rollback()
#        print('failed to add win')
#        return False


#def getPlayedGames(username):
#    cursor = sqliteConnection.cursor()
#    query = "SELECT * FROM main WHERE username = '%s'" % username
#    try:
#          cursor.execute(query)
#          result = cursor.fetchone()
#          return result[4]
#    except:
#        print('failed to get games')
#        return False


#def getWonGames(username):
#    cursor = sqliteConnection.cursor()
#    query = "SELECT * FROM main WHERE username = '%s'" % username
#    try:
#        cursor.execute(query)
#        result = cursor.fetchone()
#        return result[5]
#    except:
#        print('failed to get games')
#        return False


label = Label(root, text="***********HELLO FROM SOS GAME***********")
label.grid(row=0, column=0)

label = Label(root, text="LOG IN:")
label.grid(row=1, column=0)
label1 = tkp.Label(text="Username")
label2 = tkp.Label(text="Password")
entry1 = tkp.Entry(width=25)
entry2 = tkp.Entry(width=25)
label1.grid(row=2, column=0)
label2.grid(row=3, column=0)
entry1.grid(row=2, column=1)
entry2.grid(row=3, column=1)

nextbtn = ttk.Button(root, text="Log in", command=gameWindow)
nextbtn.grid(row=5, column=0)

label = Label(root, text="CREATE ACCOUNT")

label.grid(row=6, column=0)

label3 = tkp.Label(text="Username(admin)")
label4 = tkp.Label(text="Password(123456)")
entry3 = tkp.Entry(width=25)
entry4 = tkp.Entry(width=25)
label3.grid(row=7, column=0)
label4.grid(row=8, column=0)
entry3.grid(row=7, column=1)
entry4.grid(row=8, column=1)

next1btn = ttk.Button(root, text="Next", command=openNewWindow)
next1btn.grid(row=9, column=0)

root.mainloop()
