import sqlite3

def get_schedule(class_name, day):
    """Функция для получения расписания из базы данных"""
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    query = """
        SELECT time, subject
        FROM schedule
        WHERE class_name = ? AND day = ?
        ORDER BY time
    """
    cursor.execute(query, (class_name, day))  # Передаем правильные параметры
    rows = cursor.fetchall()

    conn.close()

    if rows:
        schedule = "\n".join([f"⏰Время: {time}, 📖 Урок: {subject}" for time, subject in rows])
        return schedule
    else:
        return f"На {day} нет расписания для класса {class_name}."
    
def get_full_week_schedule(class_name):
    """Функция для получения расписания всей недели для указанного класса"""
    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    query = """
        SELECT day, time, subject
        FROM schedule
        WHERE class_name = ?
        ORDER BY CASE 
            WHEN day = 'Понедельник' THEN 1
            WHEN day = 'Вторник' THEN 2
            WHEN day = 'Среда' THEN 3
            WHEN day = 'Четверг' THEN 4
            WHEN day = 'Пятница' THEN 5
            ELSE 6
        END, time
    """
    cursor.execute(query, (class_name,))
    rows = cursor.fetchall()

    conn.close()

    if rows:
        schedule = ""
        for day in ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']:
            schedule += f"\n{day}:\n"
            daily_schedule = [f"{time} - {subject}" for day_of_week, time, subject in rows if day_of_week == day]
            schedule += "\n".join(daily_schedule) + "\n"
        return schedule.strip()
    else:
        return f"Нет расписания для класса {class_name}."

