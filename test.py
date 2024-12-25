import sqlite3

connection = sqlite3.connect("project.db")
cursor = connection.cursor()
a = cursor.execute("PRAGMA table_info(Match);").fetchall()
print(a)






# имена колонок
# cursor.execute("PRAGMA table_info(Odds)")
# columns = [row for row in cursor.fetchall()]
# print("Имена колонок:", columns)


#https://rbvn3.com/match/38100543

# #очистить таблицу

connection.commit()
connection.close()


