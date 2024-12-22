import sqlite3

connection = sqlite3.connect("project.db")
cursor = connection.cursor()
last_datetime = ('2024-12-20 16:30:00',)
print(last_datetime[0])






# имена колонок
# cursor.execute("PRAGMA table_info(Odds)")
# columns = [row for row in cursor.fetchall()]
# print("Имена колонок:", columns)


#https://rbvn3.com/match/38100543

# #очистить таблицу
cursor.execute("DELETE FROM Urls")
cursor.execute("DELETE FROM Match")
cursor.execute("DELETE FROM Odds")
print('почистил')



connection.commit()
connection.close()


