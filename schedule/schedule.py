import sqlite3
from schedule_data import schedule_data

# Подключение к базе данных
conn = sqlite3.connect("schedule.db")
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT NOT NULL,
        day TEXT NOT NULL,
        time TEXT NOT NULL,
        subject TEXT NOT NULL
    )
''')

# Очистка таблицы (если нужно заново вставить данные)
cursor.execute("DELETE FROM schedule")

# Вставка данных
cursor.executemany('''
    INSERT INTO schedule (class_name, day, time, subject)
    VALUES (?, ?, ?, ?)
''', schedule_data)

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("Данные успешно записаны в базу данных.")
