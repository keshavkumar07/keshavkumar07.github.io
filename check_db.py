import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM attendance")
rows = cursor.fetchall()

print("\n📊 Attendance Table:\n")
print("ID | Name | Time | Date")
print("-" * 35)

for row in rows:
    print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")

conn.close()