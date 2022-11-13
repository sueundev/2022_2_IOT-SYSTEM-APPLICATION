import re
import MySQLdb as sql
from tkinter import *

app = Tk()
app.title("Guestbook using MySQL")
app.geometry("450x450+200+200")

db = sql.connect("localhost", "pi", "1234", "gb")
cur = db.cursor()
query = "SELECT * FROM info"

def refresh() :
    i = 0
    labels_time = []
    cur.execute(query)
    while True:
        result = cur.fetchone()
        if not result: break
        labels_time.append(Label(app, text=result[0]))
        labels_time[i].grid(column=0, row=3+i)
        i += 1

    j = 0
    labels_name = []
    cur.execute(query)
    while True:
        result = cur.fetchone()
        if not result: break
        labels_name.append(Label(app, text=result[1], width=10))
        labels_name[j].grid(column=1, row=3+j)
        j += 1

    k = 0
    labels_content = []
    cur.execute(query)
    while True:
        result = cur.fetchone()
        if not result: break
        labels_content.append(Label(app, text=result[2], width=30, anchor='w'))
        labels_content[k].grid(column=2, row=3+k)
        k += 1

        
def callback():
    db.commit()
    refresh()


btn = Button(app, text="Refresh", width=10, command=callback)
btn.grid(column=0, row=0)

l_time = Label(app, text="Time", bg='white')
l_time.grid(column=0, row=1)
l_name = Label(app, text="Name", bg='white')
l_name.grid(column=1, row=1)
l_content = Label(app, text="content", bg='white')
l_content.grid(column=2, row=1)

refresh()
