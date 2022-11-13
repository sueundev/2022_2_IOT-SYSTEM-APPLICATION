import MySQLdb as sql
from tkinter import *
import time
from datetime import datetime

app = Tk()
app.title("Guestbook using MySQL")
app.geometry("450x450+200+200")

def callback():
    input_name = t_name.get("1.0", END).replace("\n", "")
    print(input_name)
    input_content = t_content.get("1.0", END).replace("\n", "")
    print(input_content)
    t = datetime.now()
    time = t.strftime("%H:%M:%S")
    print(time)

    data = (time, input_name, input_content)
    cur.execute(query, data)
    db.commit()
    

db = sql.connect("localhost", "pi", "1234", "gb")
cur = db.cursor()
query = "INSERT INTO info (time, name, content) VALUES (%s, %s, %s)"

input_name = "" 
l_name = Label(app, text="Name :")
l_name.grid(column=0, row=0)
t_name = Text(app, width=45, height=1)
t_name.grid(column=1, row=0)
t_name.insert(END, "")

input_content = ""
l_content = Label(app, text="Content :")
l_content.grid(column=0, row=1)
t_content = Text(app, width=45, height=22)
t_content.grid(column=1, row=1)
t_content.insert(END, "")

btn = Button(app, text="Submit", width=10, command=callback)
btn.grid(column=1, row=2)

time = ""

app.mainloop()
