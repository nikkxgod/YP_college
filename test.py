import sqlite3

connection = sqlite3.connect("project.db")
cursor = connection.cursor()

# Вставка данных
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы:", tables)


connection.close()


