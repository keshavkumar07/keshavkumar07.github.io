import sqlite3
from datetime import datetime

today = datetime.now().strftime("%d-%m-%Y")

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM attendance WHERE date=?", (today,))
rows = cursor.fetchall()

print("\n📅 Today's Attendance:\n")

for row in rows:
    print(row)

conn.close()