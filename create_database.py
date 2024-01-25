import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('test_database.db')
cursor = connection.cursor()

# Создаем таблицу
cursor.execute('''
CREATE TABLE IF NOT EXISTS Player (
id INTEGER PRIMARY KEY,
player_id TEXT NOT NULL,
player_progress TEXT NOT NULL
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
print('db created')