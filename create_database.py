import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('questions_database.db')
cursor = connection.cursor()

# Создаем таблицу
cursor.execute('''
CREATE TABLE IF NOT EXISTS Questions (
id INTEGER PRIMARY KEY,
question TEXT NOT NULL,
answers TEXT,
right TEXT NOT NULL,
picture TEXT NOT NULL,
question_type TEXT NOT NULL
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
print('db created')