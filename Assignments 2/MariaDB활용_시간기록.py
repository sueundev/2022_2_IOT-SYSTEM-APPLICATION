import MySQLdb as sql
import RPi.GPIO as GPIO
import time
from datetime import datetime

btn = 0
pin_1 = 15
pin_2 = 18
cnt = 1

db = sql.connect("localhost", "pi", "1234", "timeTable")
cur = db.cursor()
query = "INSERT INTO dbTable (num, btn, time) VALUES (%s, %s, %s)"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(pin_2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

while True and cnt < 11 :
    if btn == 0 and GPIO.input(pin_1) == GPIO.HIGH :
        t = datetime.now()
        dt = (cnt, 'A', (str(t.year) + '-' + str(t.month) + '-' + str(t.day) + ' ' + t.strftime("%H:%M:%S")))
        cur.execute(query, dt)
        db.commit()
        cnt += 1
        btn = 1
    elif btn == 1 and GPIO.input(pin_1) == GPIO.LOW :
        btn = 0

    if btn == 0 and GPIO.input(pin_2) == GPIO.HIGH :
        t = datetime.now()
        dt = (cnt, 'B', (str(t.year) + '-' + str(t.month) + '-' + str(t.day) + ' ' + t.strftime("%H:%M:%S")))
        cur.execute(query, dt)
        db.commit()
        cnt += 1
        btn = 1
        
    elif btn == 1 and GPIO.input(pin_2) == GPIO.LOW :
        btn = 0
        
    time.sleep(0.1)

    if cnt >= 11 :
        query = "SELECT * FROM dbTable"
        cur.execute(query)
        desc = cur.description
        print("=======================================")
        print(" 순번 | 버튼 정보 |       발생 시간       |")
        print("=======================================")
        while True:
            result = cur.fetchone()
            if not result: break
            print(' ', result[0], ' |      ', result[1], ' | ', result[2], '|')
        
cur.close()
db.close()
