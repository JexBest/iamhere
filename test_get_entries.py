from database.connection import create_connection
from database.models import filter_diary_by_date_range, update_diary_entry, filter_diary_by_date, add_diary_entry




# telegram_id = input("Для тестового запроса введите телеграмм id: ")
# date = input("Введите дату за которую вы хотите найти записи в формате 'ГГГГ-ММ-ДД'")
# entries = filter_diary_by_date(telegram_id, date)
# content = input("Для тестового текст: ")
#
# diary_entries = add_diary_entry(telegram_id, content)


#посмотрим записи и запомним для работы с ними их ID
telegram_id = input("Для тестового запроса введите телеграмм id: ")
date_start = input("Введите начальную дату за которую вы хотите найти записи в формате 'ГГГГ-ММ-ДД': ")
date_end = input("Введите конечную дату за которую вы хотите найти записи в формате 'ГГГГ-ММ-ДД': ")
entries = filter_diary_by_date_range (telegram_id, date_start, date_end)

entry_id = input("Введи ID записи для редактирования: ")
new_content = input("Введите новый комментарий: ")

content = update_diary_entry(telegram_id, entry_id, new_content)
#тут выведем еще раз запись что бы убедиться что она изменилась
entries = filter_diary_by_date_range (telegram_id, date_start, date_end)

