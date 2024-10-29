from database.connection import create_connection
from database.models import filter_diary_by_date


telegram_id = input("Для тестового запроса введите телеграмм id: ")
date = input("Введите дату за которую вы хотите найти записи в формате 'ГГГГ-ММ-ДД'")

entries = filter_diary_by_date(telegram_id, date)